from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Input


class SearchModal(Screen[str]):
    """A modal screen for searching movies"""

    BINDINGS = [("escape", "app.pop_screen", "Close Search")]

    def compose(self) -> ComposeResult:
        with Container(id="search-modal"):
            yield Input(placeholder="Enter movie title...")

    def on_mount(self) -> None:
        """Focus the input when the modal is mounted"""
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Called when the user presseas Enter"""

        self.dismiss(event.value)
