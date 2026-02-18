from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static


class Column(Static):
    can_focus = True

    def __init__(self, title: str, id: str) -> None:
        # Initialize the widget with the ID
        super().__init__(id=id)
        # Apply the title to the border instead of the inside of the widget
        self.border_title = title

class YaziLayoutApp(App):
    CSS_PATH = "layout.tcss"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, ansi_color=True, **kwargs)

    def compose(self) -> ComposeResult:
        with Horizontal(id="main-container"):
            yield Column("Browse Movies", id="browse")
            yield Column("Movie Details", id="details")
            yield Column("Downloading", id="downloading")

if __name__ == "__main__":
    app = YaziLayoutApp()
    app.run()
