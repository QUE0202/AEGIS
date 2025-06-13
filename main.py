import typer
from agents.red_team import red_team_interface
from agents.blue_team import blue_team_interface

app = typer.Typer(help="🛡️ AEGIS – Red/Blue Team Local Assistant")

@app.command()
def red():
    """Run AEGIS in Red Team mode"""
    red_team_interface()

@app.command()
def blue():
    """Run AEGIS in Blue Team mode"""
    blue_team_interface()

if __name__ == "__main__":
    app()
