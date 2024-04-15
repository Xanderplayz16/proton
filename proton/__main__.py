import typer, os
from rich.progress import Progress, SpinnerColumn, TextColumn
app = typer.Typer()
projectapp = typer.Typer()
app.add_typer(projectapp, name="project")

@projectapp.command()
def init(dir:str="."):
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task("Creating project...")
        os.mkdir(dir + "/" + "src")
        os.mkdir(dir + "/" + "web")
        with open(dir + "/" + "src/main.py", "w") as f:
            f.write("import proton as pt;win = pt.Window('A Proton webapp', 'web');win.start(debug=True);document=pt.Document(wind)")
        with open(dir + "/" + "web/index.html", "w") as f:
            f.write("<!DOCTYPE html>\n<body>\n  <h1>Hello, World!</h1>\n</body>\n</html>")
if __name__ == "__main__":
    app()