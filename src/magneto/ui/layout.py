from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label, ListItem, ListView, Static

from magneto.api.yts import YTSClient
from magneto.ui.search_modal import SearchModal

NARROW_THRESHOLD = 120  # columns


class Column(Static):
    can_focus = True

    def __init__(self, title: str, id: str) -> None:
        super().__init__(id=id)
        self.border_title = title


class MovieItem(ListItem):
    def __init__(self, movie: dict) -> None:
        super().__init__()
        self.movie = movie

    def compose(self) -> ComposeResult:
        title = self.movie["title"]
        year = self.movie["year"]
        rating = self.movie["rating"]
        yield Label(f"{title} ({year}) ⭐ {rating}")


class MagnetoApp(App):
    CSS_PATH = "style.tcss"
    
    BINDINGS = [("q", "quit", "Quit"), ("/", "show_search", "Search"),]

    def __init__(self):
        super().__init__(ansi_color=True)
        self.yts = YTSClient()

    def compose(self) -> ComposeResult:
        with Container(id="main-container"):
            yield ListView(id="browse")
            yield Column("Movie Details", id="details")
            yield Column("Downloading", id="downloading")

    def action_show_search(self) -> None:
        """Show search modal screen"""
        def handle_search_query(query: str) -> None:
            if query:
                self.log(f"Searching for: {query}")

        self.push_screen(SearchModal(), handle_search_query)


    def on_resize(self, event) -> None:
        """Switch layout based on terminal width."""
        container = self.query_one("#main-container")
        if event.size.width < NARROW_THRESHOLD:
            container.styles.layout = "vertical"
        else:
            container.styles.layout = "horizontal"

    async def on_mount(self) -> None:
        browse = self.query_one("#browse", ListView)
        browse.border_title = "Browse Movies"

        # Set initial layout
        width = self.size.width
        container = self.query_one("#main-container")
        if width < NARROW_THRESHOLD:
            container.styles.layout = "vertical"
        else:
            container.styles.layout = "horizontal"

        try:
            movies = await self.yts.list_movies(limit=20)
            for movie in movies:
                browse.append(MovieItem(movie))
        except Exception as e:
            browse.append(ListItem(Label(f"Error: {e}")))
