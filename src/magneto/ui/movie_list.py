from textual.message import Message
from textual.widgets import Label, ListItem, ListView, LoadingIndicator

from magneto.api.yts import MovieListResponse, YTSClient
from magneto.ui.movie_item import MovieItem

UNCHANGED = object()
GENRES = [
    "action",
    "adventure",
    "animation",
    "biography",
    "comedy",
    "crime",
    "documentary",
    "drama",
    "family",
    "fantasy",
    "film-noir",
    "history",
    "horror",
    "music",
    "musical",
    "mystery",
    "romance",
    "sci-fi",
    "short",
    "sport",
    "thriller",
    "war",
    "western",
]


class MovieList(ListView):
    BINDINGS = [
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
    ]

    class MoviesLoaded(Message):
        """Posted when the movie list is loaded."""

        def __init__(self, movies: list[dict], total_pages: int) -> None:
            self.movies = movies
            self.total_pages = total_pages
            super().__init__()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.yts = YTSClient()
        self.current_movies: list[dict] = []
        self.current_page = 1
        self.total_pages = 1
        self.current_query: str | None = None
        self.current_genre: str | None = None

    def _update_title(self) -> None:
        parts = ["Browse Movies"]
        if self.current_query:
            parts.append(f"Search: {self.current_query}")
        if self.current_genre:
            parts.append(f"Genre: {self.current_genre.title()}")
        parts.append(f"Page {self.current_page}/{self.total_pages}")
        self.parent.border_title = " | ".join(parts)

    def _render_movies(self, movies: list[dict]) -> None:
        self.clear()
        if not movies:
            self.append(ListItem(Label("No movies found")))
            return

        for movie in movies:
            self.append(MovieItem(movie))
        self.index = 0
        self.focus()

    async def update_list(
        self,
        *,
        page: int | object = UNCHANGED,
        query: str | None | object = UNCHANGED,
        genre: str | None | object = UNCHANGED,
    ) -> None:
        target_page = self.current_page if page is UNCHANGED else int(page)
        target_query = self.current_query if query is UNCHANGED else (query.strip() or None if query else None)
        target_genre = self.current_genre if genre is UNCHANGED else genre

        previous_movies = self.current_movies
        previous_page = self.current_page
        previous_total_pages = self.total_pages
        previous_query = self.current_query
        previous_genre = self.current_genre

        self.clear()
        self.append(ListItem(LoadingIndicator()))

        try:
            response: MovieListResponse = await self.yts.list_movies(
                page=target_page,
                limit=20,
                query_term=target_query,
                genre=target_genre,
            )
            movies = response["movies"]
            movie_count = response["movie_count"]
            limit = response["limit"] or 20
            total_pages = max(1, (movie_count + limit - 1) // limit)
            if not movies and target_page > 1:
                self.current_movies = previous_movies
                self.current_page = previous_page
                self.total_pages = previous_total_pages
                self.current_query = previous_query
                self.current_genre = previous_genre
                self._render_movies(previous_movies)
                self._update_title()
                self.notify("No more movies in this result set.", severity="warning")
                return

            self.current_movies = movies
            self.current_page = target_page
            self.total_pages = total_pages
            self.current_query = target_query
            self.current_genre = target_genre
            self._render_movies(movies)
            self._update_title()
            self.post_message(self.MoviesLoaded(movies, total_pages))

        except Exception as e:
            self.current_movies = previous_movies
            self.current_page = previous_page
            self.total_pages = previous_total_pages
            self.current_query = previous_query
            self.current_genre = previous_genre
            self._render_movies(previous_movies)
            self._update_title()
            if previous_movies:
                self.notify(f"Error: {e}", severity="error")
                return

            self.clear()
            self.append(ListItem(Label(f"Error: {e}")))
            self.post_message(self.MoviesLoaded([]))

    async def on_mount(self) -> None:
        self.focus()
        self._update_title()
        self.run_worker(self.update_list())
