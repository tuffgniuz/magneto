from textual.containers import Container


class Column(Container):
    can_focus = False

    def __init__(self, title: str, *children, id: str) -> None:
        super().__init__(*children, id=id)
        self.border_title = title
