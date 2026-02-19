from textual.widgets import Label, ListItem


class TorrentItem(ListItem):
    def __init__(self, torrent: dict) -> None:
        super().__init__()
        self.torrent = torrent

    def compose(self) -> None:
        quality = self.torrent["quality"]
        torrent_type = self.torrent["type"]
        size = self.torrent["size"]
        seeds = self.torrent["seeds"]
        peers = self.torrent["peers"]
        yield Label(f"{quality} {torrent_type} | {size} | Seeds: {seeds} Peers: {peers}")
