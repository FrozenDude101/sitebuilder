from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from os import PathLike
    from typing import Self

from html.parser import HTMLParser
from pathlib import Path

from .Logging import logger
_logger = logger.getChild("template")


class Template(HTMLParser):

    def __init__(self, name, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.name = name
        self.data = ""
        self.slots: dict[str, int] = {}

    def feed(self, data: str) -> Self:
        self.data += data
        super().feed(data)
        return self

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if not tag.startswith("sbt-"): return
        slotName = tag[4:]
        if slotName not in self.slots: self.slots[slotName] = 0
        self.slots[tag[4:]] += 1

    def replace(self, key: str, new: str) -> Template:
        if key not in self.slots:
            _logger.warn(f"Slot key '{key}' not found in template '{self.name}'.")
        return Template(self.name).feed(self.data.replace(f"<sbt-{key}/>", new))