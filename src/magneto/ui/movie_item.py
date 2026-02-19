from textual.app import ComposeResult
from textual.widgets import Label, ListItem


class MovieItem(ListItem):
    def __init__(self, movie: dict) -> None:
        super().__init__()
        self.movie = movie

    def compose(self) -> ComposeResult:
        title = self.movie["title"]
        year = self.movie["year"]
        rating = self.movie["rating"]
        yield Label(f"{title} ({year}) ⭐ {rating}")

