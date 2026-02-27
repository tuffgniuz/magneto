import sys
from pathlib import Path


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
