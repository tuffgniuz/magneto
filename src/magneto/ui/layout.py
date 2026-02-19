from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label, ListItem, ListView, LoadingIndicator, Static

from magneto.api.yts import YTSClient
from magneto.ui.column import Column
from magneto.ui.movie_item import MovieItem
from magneto.ui.search_modal import SearchModal

NARROW_THRESHOLD = 120  # columns


class MagnetoApp(App):
    CSS_PATH = "style.tcss"
    
    BINDINGS = [
        ("q", "quit", "Quit"), 
        ("/", "show_search", "Search"),
        ("c", "clear_search", "Clear search")
    ]

    def __init__(self):
        super().__init__(ansi_color=True)
        self.yts = YTSClient()

    def compose(self) -> ComposeResult:
        with Container(id="main-container"):
            yield ListView(id="browse")
            yield Column("Movie Details", id="details")
            yield Column("Downloading", id="downloading")

    async def update_browse_list(self, query: str | None = None) -> None:
        browse_list = self.query_one("#browse", ListView)
        browse_list.clear()

        browse_list.append(ListItem(LoadingIndicator()))

        try:
            movies = await self.yts.list_movies(limit=20, query_term=query)
            browse_list.clear()

            if not movies:
                browse_list.append(ListItem(Label("No movies found")))
                return

            for movie in movies:
                browse_list.append(MovieItem(movie))

        except Exception as e:
            browse_list.clear()
            browse_list.append(ListItem(Label(f"Error: {e}")))

    def action_show_search(self) -> None:
        """Show search modal screen"""
        def handle_search_query(query: str) -> None:
            if query:
                self.run_worker(self.update_browse_list(query))

        self.push_screen(SearchModal(), handle_search_query)

    def action_clear_search(self) -> None:
        self.run_worker(self.update_browse_list())

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
        
        self.run_worker(self.update_browse_list())
