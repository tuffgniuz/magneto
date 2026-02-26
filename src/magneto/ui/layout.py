import subprocess
import sys

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import ListView

from magneto.api.yts import YTSClient
from magneto.ui.column import Column
from magneto.ui.movie_details import MovieDetails
from magneto.ui.movie_item import MovieItem
from magneto.ui.movie_list import MovieList
from magneto.ui.search_modal import SearchModal
from magneto.ui.torrent_modal import TorrentModal

NARROW_THRESHOLD = 120  # columns


class MagnetoApp(App):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("/", "show_search", "Search"),
        ("c", "clear_search", "Clear search"),
        ("t", "show_torrents", "Torrent modal"),
    ]

    def __init__(self):
        super().__init__(ansi_color=True)
        self.yts = YTSClient()
        self.movie_cache = {}

    def compose(self) -> ComposeResult:
        with Container(id="main-container"):
            yield MovieList(id="browse")
            yield Column("Movie Details", MovieDetails(id="details"), id="details-column")
            # yield Column("Downloading", id="downloading-column")

    def open_magnet_link(self, magnet_link: str) -> None:
        """Open a magnet link with the default torrent client."""
        try:
            if sys.platform == "win32":
                subprocess.Popen(["start", magnet_link], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", magnet_link])
            else:
                subprocess.Popen(["xdg-open", magnet_link])
        except FileNotFoundError:
            self.notify("Could not find a torrent client.", severity="error")

    async def fetch_and_cache_details(self, movie_id: int) -> None:
        """Fetch movie details and cache them."""
        details = await self.yts.get_movie_details(movie_id)
        self.movie_cache[movie_id] = details

        # If the fetched movie is currently highlighted, update the details pane
        browse_list = self.query_one("#browse", MovieList)
        highlighted_item = browse_list.highlighted_child
        if highlighted_item and isinstance(highlighted_item, MovieItem):
            if highlighted_item.movie["id"] == movie_id:
                details_pane = self.query_one("#details", MovieDetails)
                details_pane.update_details(details)

    async def on_movie_list_movies_loaded(self, message: MovieList.MoviesLoaded) -> None:
        """When the movie list is loaded, pre-fetch all details."""
        self.movie_cache.clear()
        for movie in message.movies:
            self.run_worker(self.fetch_and_cache_details(movie["id"]))

    async def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """When a movie is highlighted, display its details from the cache."""
        if isinstance(event.item, MovieItem):
            movie_id = event.item.movie["id"]
            details_pane = self.query_one("#details", MovieDetails)
            if movie_id in self.movie_cache:
                details_pane.update_details(self.movie_cache[movie_id])
            else:
                details_pane.update("Loading...")

    def action_show_torrents(self) -> None:
        browse_list = self.query_one("#browse", MovieList)
        highlighted_item = browse_list.highlighted_child
        if isinstance(highlighted_item, MovieItem):
            movie_id = highlighted_item.movie["id"]
            if movie_id in self.movie_cache:
                movie_data = self.movie_cache[movie_id]
                torrents = movie_data.get("torrents", [])
                title = movie_data.get("title_long", "Torrents")
                if torrents:
                    self.push_screen(TorrentModal(title, torrents))

    def action_show_search(self) -> None:
        """Show search modal screen"""
        browse_list = self.query_one("#browse", MovieList)

        def handle_search_query(query: str) -> None:
            if query:
                browse_list.run_worker(browse_list.update_list(query))

        self.push_screen(SearchModal(), handle_search_query)

    def action_clear_search(self) -> None:
        browse_list = self.query_one("#browse", MovieList)
        browse_list.run_worker(browse_list.update_list())

    def on_resize(self, event) -> None:
        """Switch layout based on terminal width."""
        container = self.query_one("#main-container")
        if event.size.width < NARROW_THRESHOLD:
            container.styles.layout = "vertical"
        else:
            container.styles.layout = "horizontal"

    async def on_mount(self) -> None:
        # Set initial layout
        width = self.size.width
        container = self.query_one("#main-container")
        if width < NARROW_THRESHOLD:
            container.styles.layout = "vertical"
        else:
            container.styles.layout = "horizontal"
