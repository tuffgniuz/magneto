from textual.message import Message
from textual.widgets import Label, ListItem, ListView, LoadingIndicator

from magneto.api.yts import YTSClient
from magneto.ui.movie_item import MovieItem


class MovieList(ListView):
    class MoviesLoaded(Message):
        """Posted when the movie list is loaded."""

        def __init__(self, movies: list[dict]) -> None:
            self.movies = movies
            super().__init__()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.yts = YTSClient()

    async def update_list(self, query: str | None = None) -> None:
        self.clear()
        self.append(ListItem(LoadingIndicator()))

        try:
            movies = await self.yts.list_movies(limit=20, query_term=query)
            self.clear()

            if not movies:
                self.append(ListItem(Label("No movies found")))
                return

            for movie in movies:
                self.append(MovieItem(movie))

            self.post_message(self.MoviesLoaded(movies))

        except Exception as e:
            self.clear()
            self.append(ListItem(Label(f"Error: {e}")))

    async def on_mount(self) -> None:
        self.border_title = "Browse Movies"
        self.run_worker(self.update_list())
