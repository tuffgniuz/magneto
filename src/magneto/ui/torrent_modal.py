from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import ListView

from magneto.ui.torrent_item import TorrentItem


class TorrentModal(Screen):

    BINDINGS = [("escape", "app.pop_screen", "Close")]

    def __init__(self, title: str, torrents: list[dict]) -> None:
        super().__init__()
        self.modal_title = title
        self.torrents = torrents

    def compose(self) -> ComposeResult:
        yield ListView(id="torrent-modal")

    def on_mount(self) -> None:
        list_view = self.query_one("#torrent-modal", ListView)
        list_view.border_title = self.modal_title
        for torrent in self.torrents:
            list_view.append(TorrentItem(torrent))
        list_view.focus()

