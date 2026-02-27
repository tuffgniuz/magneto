from textual.widgets import Static


class MovieDetails(Static):
    """A widget to display movie details."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_details(self, movie: dict) -> None:
        """Update the details displayed in the widget."""
        if not movie:
            self.update("No details available.")
            return

        genres = ", ".join(movie.get("genres", []))
        language = movie.get("language", "N/A")
        
        cast = ", ".join([actor["name"] for actor in movie.get("cast", [])[:5]])


        self.update(
            f"[b]{movie['title_long']}[/b]\n\n"
            f"Rating: {movie['rating']} | Genres: {genres} | Language: {language}\n\n"
            f"Cast: {cast}\n\n"
            f"{movie['description_full']}"
        )
