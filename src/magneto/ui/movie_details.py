from textual.containers import Container, VerticalScroll
from textual.widgets import Static
from textual_image.widget import Image


class MovieDetails(VerticalScroll):
    """A widget to display movie details."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self):
        with Container(id="details-body"):
            with Container(id="details-poster-container"):
                yield Image(None, id="details-poster")
            yield Static("No details available.", id="details-text")

    def show_message(self, message: str) -> None:
        """Display a plain message without a poster preview."""
        poster = self.query_one("#details-poster", Image)
        details_text = self.query_one("#details-text", Static)
        poster.display = False
        details_text.update(message)

    def update_details(self, movie: dict) -> None:
        """Update the details displayed in the widget."""
        poster = self.query_one("#details-poster", Image)
        details_text = self.query_one("#details-text", Static)

        if not movie:
            self.show_message("No details available.")
            return

        genres = ", ".join(movie.get("genres", []))
        language = movie.get("language", "N/A")
        cast = ", ".join(actor["name"] for actor in movie.get("cast", [])[:5]) or "N/A"
        trailer_code = movie.get("yt_trailer_code")
        trailer_status = movie.get("trailer_status", "Not available")
        poster_path = movie.get("poster_path")
        poster.display = bool(poster_path)
        poster.image = poster_path

        details_text.update(
            f"[b]{movie.get('title_long', movie.get('title', 'Unknown Title'))}[/b]\n\n"
            f"Rating: {movie.get('rating', 'N/A')} | Genres: {genres or 'N/A'} | Language: {language}\n\n"
            f"Trailer: {trailer_status}"
            f"{' | Press w to watch' if trailer_code else ''}\n\n"
            f"Cast: {cast}\n\n"
            f"{movie.get('description_full') or 'No description available.'}"
        )
