from textual.widgets import Static


class Column(Static):
    can_focus = True

    def __init__(self, title: str, id: str) -> None:
        super().__init__(id=id)
        self.border_title = title

