import os.path
from rich.theme import Theme

# happy jar path definitions
HOME = os.path.expanduser("~")
DATA_PATH = os.path.join(f"{HOME}/.happyjar.json")
OLD_DATA_PATH = os.path.join(f"{HOME}/.happyjar.txt")

THEME = Theme(
    {
        "info": "bold color(39)",
        "error": "bold red",
        "date": "bold color(111)",
        "message": "default",
        "tags": "bold color(141)",
        "warning": "italic dim yellow",
    }
)

FLOWERS = ["🌼 ", "🍀 ", "🌻 ", "🌺 ", "🌹 ", "🌸 ", "🌷 ", "💐 ", "🏵️  "]
