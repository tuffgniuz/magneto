import subprocess
import sys
from shutil import which

import httpx
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import ListView

from magneto.api.yts import YTSClient
from magneto.ui.column import Column
from magneto.ui.movie_details import MovieDetails
from magneto.ui.movie_item import MovieItem
from magneto.ui.movie_list import MovieList
from magneto.ui.genre_modal import GenreModal
from magneto.ui.search_modal import SearchModal
from magneto.utils import get_asset_path, get_poster_cache_path, get_torrent_cache_path
from magneto.ui.torrent_modal import TorrentModal

NARROW_THRESHOLD = 120  # columns


class MagnetoApp(App):
    CSS_PATH = get_asset_path("magneto/ui/style.tcss")

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("/", "show_search", "Search"),
        ("f", "show_genres", "Filter genre"),
        ("c", "clear_search", "Clear search"),
        ("l", "next_page", "Next page"),
        ("h", "previous_page", "Previous page"),
        ("w", "watch_trailer", "Watch trailer"),
        ("t", "show_torrents", "Torrent modal"),
    ]

    def __init__(self):
        super().__init__(ansi_color=True)
        self.yts = YTSClient()
        self.movie_cache = {}
        self.cache_generation = 0

    def compose(self) -> ComposeResult:
        with Container(id="main-container"):
            yield Column("Browse Movies", MovieList(id="browse"), id="browse-column")
            yield Column("Movie Details", MovieDetails(id="details"), id="details-column")
            # yield Column("Downloading", id="downloading-column")

    def _apply_responsive_layout(self, width: int) -> None:
        """Update container and child sizing for the current screen width."""
        container = self.query_one("#main-container", Container)
        details_pane = self.query_one("#details", MovieDetails)

        if width < NARROW_THRESHOLD:
            container.remove_class("wide")
            container.add_class("narrow")
            details_pane.remove_class("wide")
            details_pane.add_class("narrow")
        else:
            container.remove_class("narrow")
            container.add_class("wide")
            details_pane.remove_class("narrow")
            details_pane.add_class("wide")

    def open_magnet_link(self, magnet_link: str) -> None:
        """Open a magnet link with the default torrent client."""
        try:
            if sys.platform == "win32":
                subprocess.Popen(
                    ["start", magnet_link],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
            elif sys.platform == "darwin":
                subprocess.Popen(
                    ["open", magnet_link],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
            else:
                subprocess.Popen(
                    ["xdg-open", magnet_link],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
        except FileNotFoundError:
            self.notify("Could not find a torrent client.", severity="error")

    def open_url(self, url: str) -> None:
        """Open a URL with the default system handler."""
        try:
            self.notify("Opening trailer in browser...", severity="information")
            if sys.platform == "win32":
                subprocess.Popen(
                    ["start", url],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
            elif sys.platform == "darwin":
                subprocess.Popen(
                    ["open", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
            else:
                subprocess.Popen(
                    ["xdg-open", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
        except FileNotFoundError:
            self.notify("Could not open the URL.", severity="error")

    def open_path(self, path: str) -> None:
        """Open a local file path with the default system handler."""
        try:
            if sys.platform == "win32":
                subprocess.Popen(
                    ["start", path],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
            elif sys.platform == "darwin":
                subprocess.Popen(
                    ["open", path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
            else:
                subprocess.Popen(
                    ["xdg-open", path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
        except FileNotFoundError:
            self.notify("Could not open the file.", severity="error")

    def play_trailer(self, trailer_url: str) -> None:
        """Play the trailer in mpv if available, otherwise open it in the browser."""
        mpv_path = which("mpv")
        if mpv_path:
            try:
                self.notify("Launching mpv for trailer playback...", severity="information")
                subprocess.Popen(
                    [mpv_path, trailer_url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                )
                return
            except OSError:
                self.notify("Could not launch mpv. Falling back to browser.", severity="warning")

        self.open_url(trailer_url)

    async def cache_movie_poster(self, movie: dict) -> str | None:
        """Download and cache a poster image for the movie if available."""
        poster_url = movie.get("large_cover_image") or movie.get("medium_cover_image")
        if not poster_url:
            return None

        poster_path = get_poster_cache_path(movie["id"], poster_url)
        if poster_path.exists():
            return str(poster_path)

        async with httpx.AsyncClient(
            follow_redirects=True,
            headers=self.yts.HEADERS,
            timeout=15.0,
        ) as client:
            response = await client.get(poster_url)
            response.raise_for_status()
            poster_path.write_bytes(response.content)

        return str(poster_path)

    async def cache_torrent_file(self, torrent: dict) -> str | None:
        """Download and cache a torrent file if a direct URL is available."""
        torrent_url = torrent.get("url")
        torrent_hash = torrent.get("hash")
        if not torrent_url or not torrent_hash:
            return None

        torrent_path = get_torrent_cache_path(torrent_hash, torrent_url)
        if torrent_path.exists():
            return str(torrent_path)

        async with httpx.AsyncClient(
            follow_redirects=True,
            headers=self.yts.HEADERS,
            timeout=30.0,
        ) as client:
            response = await client.get(torrent_url)
            response.raise_for_status()
            torrent_path.write_bytes(response.content)

        return str(torrent_path)

    async def open_torrent(self, torrent: dict, movie_title: str) -> None:
        """Open a torrent client using a torrent file when possible, otherwise fall back to magnet."""
        torrent_path = await self.cache_torrent_file(torrent)
        if torrent_path:
            self.notify("Opening torrent in your default client...", severity="information")
            self.open_path(torrent_path)
            return

        self.notify("Torrent file unavailable. Falling back to magnet link...", severity="warning")
        magnet_link = TorrentModal.construct_magnet_link(torrent, movie_title)
        self.open_magnet_link(magnet_link)

    async def fetch_and_cache_details(self, movie_id: int, generation: int) -> None:
        """Fetch movie details and cache them."""
        try:
            details = await self.yts.get_movie_details(movie_id)
            details["poster_path"] = await self.cache_movie_poster(details)
            details["trailer_status"] = (
                "Available via mpv" if details.get("yt_trailer_code") and which("mpv") else
                "Available via browser" if details.get("yt_trailer_code") else
                "Not available"
            )
        except Exception:
            if generation != self.cache_generation:
                return

            self.movie_cache[movie_id] = {}
            browse_list = self.query_one("#browse", MovieList)
            highlighted_item = browse_list.highlighted_child
            if highlighted_item and isinstance(highlighted_item, MovieItem):
                if highlighted_item.movie["id"] == movie_id:
                    details_pane = self.query_one("#details", MovieDetails)
                    details_pane.show_message("Unable to load movie details.")
            return

        if generation != self.cache_generation:
            return

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
        self.cache_generation += 1
        self.movie_cache.clear()
        details_pane = self.query_one("#details", MovieDetails)
        if not message.movies:
            details_pane.show_message("No details available.")
            return

        details_pane.show_message("Loading...")
        for movie in message.movies:
            self.run_worker(self.fetch_and_cache_details(movie["id"], self.cache_generation))

    async def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """When a movie is highlighted, display its details from the cache."""
        if isinstance(event.item, MovieItem):
            movie_id = event.item.movie["id"]
            details_pane = self.query_one("#details", MovieDetails)
            if movie_id in self.movie_cache:
                details_pane.update_details(self.movie_cache[movie_id])
            else:
                details_pane.show_message("Loading...")

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
                else:
                    self.notify("No torrents available for the selected movie.", severity="warning")
            else:
                self.notify("Movie details are still loading.", severity="information")

    def action_watch_trailer(self) -> None:
        browse_list = self.query_one("#browse", MovieList)
        highlighted_item = browse_list.highlighted_child
        if not isinstance(highlighted_item, MovieItem):
            self.notify("No movie selected.", severity="warning")
            return

        movie_id = highlighted_item.movie["id"]
        movie_data = self.movie_cache.get(movie_id)
        if not movie_data:
            self.notify("Movie details are still loading.", severity="information")
            return

        trailer_code = movie_data.get("yt_trailer_code")
        if not trailer_code:
            self.notify("No trailer available for the selected movie.", severity="warning")
            return

        self.play_trailer(f"https://www.youtube.com/watch?v={trailer_code}")

    def action_show_search(self) -> None:
        """Show search modal screen"""
        browse_list = self.query_one("#browse", MovieList)

        def handle_search_query(query: str) -> None:
            if query:
                browse_list.run_worker(browse_list.update_list(page=1, query=query))

        self.push_screen(SearchModal(), handle_search_query)

    def action_show_genres(self) -> None:
        browse_list = self.query_one("#browse", MovieList)

        def handle_genre_selection(genre: str | None) -> None:
            browse_list.run_worker(browse_list.update_list(page=1, genre=genre))

        self.push_screen(GenreModal(), handle_genre_selection)

    def action_clear_search(self) -> None:
        browse_list = self.query_one("#browse", MovieList)
        browse_list.run_worker(browse_list.update_list(page=1, query=None))

    def action_next_page(self) -> None:
        browse_list = self.query_one("#browse", MovieList)
        browse_list.run_worker(browse_list.update_list(page=browse_list.current_page + 1))

    def action_previous_page(self) -> None:
        browse_list = self.query_one("#browse", MovieList)
        if browse_list.current_page == 1:
            self.notify("Already on the first page.", severity="information")
            return
        browse_list.run_worker(browse_list.update_list(page=browse_list.current_page - 1))

    def on_resize(self, event) -> None:
        """Switch layout based on terminal width."""
        self._apply_responsive_layout(event.size.width)

    async def on_mount(self) -> None:
        self._apply_responsive_layout(self.size.width)
        self.query_one("#browse", MovieList).focus()
