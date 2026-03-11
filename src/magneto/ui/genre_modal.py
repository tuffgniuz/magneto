from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView

from magneto.ui.movie_list import GENRES


class GenreItem(ListItem):
    def __init__(self, genre: str | None, label: str) -> None:
        super().__init__(Label(label))
        self.genre = genre


class GenreList(ListView):
    BINDINGS = [
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
    ]


class GenreModal(Screen[str | None]):
    """A modal screen for selecting a movie genre."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Close"),
        ("enter", "select_genre", "Select"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="genre-modal"):
            yield GenreList(
                GenreItem(None, "All Genres"),
                *[GenreItem(genre, genre.title()) for genre in GENRES],
                id="genre-list",
            )

    def on_mount(self) -> None:
        genre_list = self.query_one("#genre-list", ListView)
        genre_list.focus()
        genre_list.index = 0

    def action_select_genre(self) -> None:
        genre_list = self.query_one("#genre-list", ListView)
        highlighted_item = genre_list.highlighted_child
        if isinstance(highlighted_item, GenreItem):
            self.dismiss(highlighted_item.genre)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, GenreItem):
            self.dismiss(event.item.genre)
