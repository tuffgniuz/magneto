import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse


def get_asset_path(relative_path: str) -> Path:
    """
    Get the absolute path to a bundled asset.

    Args:
        relative_path: The relative path to the asset.

    Returns:
        The absolute path to the asset.
    """
    if getattr(sys, "frozen", False):
        # We are running in a bundled environment (e.g., PyInstaller)
        base_path = Path(sys._MEIPASS)
    else:
        # We are running in a normal Python environment
        base_path = Path(__file__).parent.parent.resolve()

    return base_path / relative_path


def get_poster_cache_path(movie_id: int, image_url: str) -> Path:
    """Return a stable cache path for a downloaded poster image."""
    suffix = Path(urlparse(image_url).path).suffix or ".jpg"
    cache_dir = Path(tempfile.gettempdir()) / "magneto-posters"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{movie_id}{suffix}"


def get_torrent_cache_path(torrent_hash: str, torrent_url: str) -> Path:
    """Return a stable cache path for a downloaded torrent file."""
    suffix = Path(urlparse(torrent_url).path).suffix or ".torrent"
    cache_dir = Path(tempfile.gettempdir()) / "magneto-torrents"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{torrent_hash}{suffix}"
