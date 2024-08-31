import rich.style
import typer, os, platform, shutil, rich, sys, toml
from rich.progress import Progress, SpinnerColumn, TextColumn
import subprocess as sp
from rich.panel import Panel
from rich import print as rprint
from .core.utils import remove_files
app = typer.Typer()
projectapp = typer.Typer(help="Project management.")
app.add_typer(projectapp, name="project")

def error(text:str):
    rprint(Panel(text, title="[red]Error", title_align="left", style=rich.style.Style(color = "red")))

@projectapp.command()
def run():
    if '__compiled__' in globals():
        error('Running from compiled executable.\nThis could cause Proton to call the compiled that calls Proton... etc.\nThis is basically a forkbomb.')
        return
        
    os.system(f"{sys.executable} src/main.py")

@projectapp.command()
def init(dir:str="."):
    """Initalizes a new project."""
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Creating project...")
        os.mkdir(os.path.join(dir, 'src'))
        os.mkdir(os.path.join(dir, 'web'))
        with open(os.path.join(dir, 'src', 'main.py')) as f:
            f.write("import proton as pt\nwin = pt.Window('A Proton webapp', '../web')\nwin.start(debug=True)\ndocument=win.document")
        with open(os.path.join(dir, 'web', 'index.html'), "w") as f:
            f.write("<!DOCTYPE html>\n<body>\n  <h1>Hello, World!</h1>\n</body>\n</html>")
        with open(os.path.join(dir, 'project.toml'), 'w') as f:
            f.write("""[proton]
                    entrypoint = "src/main.py"
                    
                    [proton.build]
                    verbose = false
                    windows_disable_console = true
                    datafiles = ["web"]
                    
                    [proton.build.bloat]
                    disable_qt = true
                    disable_gtk = false
                    experimental_bloat_removal = true""")



@projectapp.command()
def build():
    """Build your project."""
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        with open('project.toml', 'r') as f:
            cfg = toml.load(f)
        try: experimental_bloat_removal = cfg["proton"]["build"]["bloat"]["experimental_bloat_removal"]
        except Exception: experimental_bloat_removal = False
        try: disable_qt = cfg["proton"]["build"]["bloat"]["disable_qt"]
        except Exception: disable_qt = True
        try: disable_gtk = cfg["proton"]["build"]["bloat"]["disable_gtk"]
        except Exception: disable_gtk = True
        try: verbose = cfg["proton"]["build"]["verbose"]
        except Exception: verbose = False
        try: entrypoint = cfg["proton"]["entrypoint"]
        except Exception: print('Please set entrypoint in project.toml'); exit()
        try: datafiles = cfg["proton"]["build"]["datafiles"]
        except Exception: datafiles = []
        try: windows_disable_console = cfg["proton"]["build"]["windows_disable_console"]
        except Exception: windows_disable_console = False
        extra_args = ""
        if experimental_bloat_removal:
            print('WARNING: You are using experimental bloat removal, and this may cause all kinds of issues.')
        if experimental_bloat_removal and (os.name == 'nt'):
            error('Experimental bloat removal does nothing on windows, as there aren\'t too many unnessecary libraries that can be removed.'); exit()
        if disable_qt:
            extra_args += '--nofollow-import-to=PySide6 --nofollow-import-to=qtpy --nofollow-import-to=PySide2 '
        else:
            extra_args += '--enable-plugin=pyside6 '
        if disable_gtk:
            extra_args += '--nofollow-import-to=gi '
        if verbose:
            extra_args += '--verbose '
        if windows_disable_console and os.name == 'nt': # Disabling the console does nothing on non-Windows systems.
            extra_args += '--disable-console '
        if platform.system() == "Darwin":
            # macos
            extra_args += '--macos-create-app-bundle '
        try:
            shutil.rmtree("dist")
        except Exception:
            pass
        progress.add_task("Building...", total = 2)
        print("")
        print("")
        
        
        p = sp.Popen(f"python -m nuitka {entrypoint} --standalone --nofollow-import-to=cefpython3 --nofollow-import-to=kivy --nofollow-import-to=jnius --nofollow-import-to=PyQt5 {extra_args} 2>&1", shell=True, stdout = sp.PIPE, stderr = sp.DEVNULL)
        prev = b''
        while p.poll() == None: # TODO: find out why this doesn't work on windows
            a = p.stdout.read(1)
            prev = prev+a
            if a == b'\n':
                print(prev.decode()[:-1])
                prev = b''
        if p.poll() != 0:
            print('ERROR: Nuitka exited with non-zero exit code '+str(p.poll()))
            exit(51)
        
        
        #try:
        #    os.mkdir("dist")
        #except FileExistsError:
        #    pass
        
        shutil.rmtree("main.build")
        if platform.system() == "Darwin":
            os.mkdir("dist")
            app = [i for i in os.listdir if i.endswith(".app")][0]
            shutil.copytree(app, os.path.join('dist', app))
            for i in datafiles:
                shutil.copytree({i}, os.path.join('dist', app, 'Contents', 'MacOS', {i}))
            shutil.rmtree(app)
        else:
            shutil.move("main.dist", "dist")
            for i in datafiles:
                shutil.copytree(i, os.path.join('dist', i))
        
        if experimental_bloat_removal:
            files = "libncursesw.so.6 libssl.so.3 libuuid.so.1 libbz2.so.1.0 libgcc_s.so.1 libcrypto.so.3 libpcre2-8.so.0 gevent girepository greenlet cryptography _brotli.so libglib-2.0.so.0"
            for i in files.split(' '):
                try:
                    remove_files("dist/"+i)
                except FileNotFoundError:
                    if verbose:
                        print(f'Experimental bloat removal: File {i} does not exist!')
        
    print("Done!")
        
if __name__ == "__main__":
    app()