from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from os import PathLike

from pathlib import Path
import json

from .Logging import logger
_logger = logger.getChild("meta")


class MetaFile():

    _NAME = "meta.json"

    def __init__(self, template=None) -> None:
        self.template = template

    @staticmethod
    def load(path: str|PathLike) -> MetaFile:
        path = Path(path)/MetaFile._NAME
        
        try:
            with open(path) as f:
                raw: dict = json.load(f)
        except FileNotFoundError:
            _logger.debug("No file found at %s, using default meta values.", path)
            return MetaFile()
        except json.JSONDecodeError as e:
            _logger.debug(e)
            _logger.warn("Problem parsing %s, using default meta values.", path)
            return MetaFile()
        
        template = raw.get("template")
        
        return MetaFile(
            template=template
        )
    
    def getTemplate(self) -> str|None:
        return self.template