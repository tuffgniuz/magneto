from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import ListView

from magneto.ui.torrent_item import TorrentItem


class TorrentModal(Screen):

    BINDINGS = [
        ("escape", "app.pop_screen", "Close"),
        ("d", "download_torrent", "Download"),
    ]

    def __init__(self, title: str, torrents: list[dict]) -> None:
        super().__init__()
        self.modal_title = title
        self.torrents = torrents

    def compose(self) -> ComposeResult:
        yield ListView(*[TorrentItem(t, self.modal_title) for t in self.torrents], id="torrent-modal")

    def on_mount(self) -> None:
        list_view = self.query_one(ListView)
        list_view.border_title = self.modal_title
        list_view.focus()

    def action_download_torrent(self) -> None:
        """Handle the download torrent action."""
        list_view = self.query_one(ListView)
        highlighted_item = list_view.highlighted_child
        if isinstance(highlighted_item, TorrentItem):
            magnet_link = self._construct_magnet_link(
                highlighted_item.torrent, highlighted_item.movie_title
            )
            self.app.open_magnet_link(magnet_link)
            self.app.pop_screen()

    def _construct_magnet_link(self, torrent: dict, movie_title: str) -> str:
        """Construct the magnet link from torrent data."""
        hash_ = torrent["hash"]
        dn = movie_title
        trackers = [
            "udp://glotorrents.pw:6969/announce",
            "udp://tracker.opentrackr.org:1337/announce",
            "udp://torrent.gresille.org:80/announce",
            "udp://tracker.openbittorrent.com:80",
            "udp://tracker.coppersurfer.tk:6969",
            "udp://tracker.leechers-paradise.org:6969",
            "udp://p4p.arenabg.ch:1337",
            "udp://tracker.internetwarriors.net:1337",
        ]

        magnet_link = f"magnet:?xt=urn:btih:{hash_}&dn={dn}"
        for tracker in trackers:
            magnet_link += f"&tr={tracker}"

        return magnet_link

