import rich.style
import typer, os, shutil, rich, sys
from rich.progress import Progress, SpinnerColumn, TextColumn
import subprocess as sp
from rich.panel import Panel
from rich import print as rprint
app = typer.Typer()
projectapp = typer.Typer(help="Project management.")
app.add_typer(projectapp, name="project")

@projectapp.command()
def run():
    os.system(f"{sys.executable} src/main.py")

@projectapp.command()
def init(dir:str="."):
    """Initalizes a new project."""
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Creating project...")
        os.mkdir(dir + "/" + "src")
        os.mkdir(dir + "/" + "web")
        with open(dir + "/" + "src/main.py", "w") as f:
            f.write("import proton as pt\nwin = pt.Window('A Proton webapp', '../web')\nwin.start(debug=True)\ndocument=win.document")
        with open(dir + "/" + "web/index.html", "w") as f:
            f.write("<!DOCTYPE html>\n<body>\n  <h1>Hello, World!</h1>\n</body>\n</html>")

def error(text:str):
    rprint(Panel(text, title="[red]Error", title_align="left", style=rich.style.Style(color = "red")))

@projectapp.command()
def build(disable_qt: bool = True, disable_gtk: bool = False, verbose: bool = True, disable_console: bool = True):
    """Build your project."""
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        extra_args = ""
        if disable_qt:
            extra_args += '--nofollow-import-to=PySide6 --nofollow-import-to=qtpy --nofollow-import-to=PySide2 '
        else:
            extra_args += '--enable-plugin=pyside6 '
        if disable_gtk:
            extra_args += '--nofollow-import-to=gi '
        if verbose:
            extra_args += '--verbose '
        if disable_console:
            extra_args += '--disable-console '
        try:
            shutil.rmtree("dist")
        except Exception:
            pass
        progress.add_task("Building...", total = 2)
        print("")
        print("")
        
        
        p = sp.Popen(f"python -m nuitka src/main.py --standalone --nofollow-import-to=cefpython3 --nofollow-import-to=kivy --nofollow-import-to=jnius --nofollow-import-to=PyQt5 {extra_args} 2>&1", shell=True, stdout = sp.PIPE, stderr = sp.DEVNULL)
        #else:
        #    error("[white]Build mode " + mode + " does not exist, quitting.\nUse build mode debug or release. (debug enables the console, while release doesn't, but release enables optimizations.)")
        #    
        #    exit()
        prev = b''
        while p.poll() == None:
            a = p.stdout.read(1)
            prev = prev+a
            if a == b'\n':
                print(prev.decode()[:-1])
                prev = b''
        if p.poll() != 0:
            print('Nuitka exited with error code '+str(p.poll()))
            exit(51)
        
        
        #try:
        #    os.mkdir("dist")
        #except FileExistsError:
        #    pass
        shutil.rmtree("main.build")
        shutil.move("main.dist", "dist")
        shutil.copytree("web", "dist/web")
        
    print("Done!")
        
if __name__ == "__main__":
    app()