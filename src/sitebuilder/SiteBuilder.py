from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from os import PathLike

import os
from pathlib import Path

from .Logging import logger
from .MetaFile import MetaFile
_logger = logger.getChild("build")

class SiteBuilder():

    def __init__(self, src: str|PathLike, dest: str|PathLike) -> None:
        self.src  = Path(src)
        self.dest = Path(dest)

        self.meta:     dict[Path, MetaFile] = {}
        self.rawFiles: dict[Path, str]      = {}
        self.files:    dict[Path, str]      = {}

    def _loadSource(self) -> None:
        os.chdir(self.src)

        for (path, _, fnames) in Path().walk():
            self.meta[path] = MetaFile.load(path)
            for fn in fnames:
                if fn == MetaFile._NAME: continue
                try:
                    with open(path/fn) as f:
                        self.rawFiles[path/fn] = f.read()
                except FileNotFoundError:
                    continue

        os.chdir("..")

    def _saveBuild(self) -> None:
        self.dest.mkdir()
        os.chdir(self.dest)

        for (path, file) in self.files.items():
            try:
                path.parent.mkdir(parents=True)
            except FileExistsError:
                pass
            with open(path, "w") as f:
                f.write(file)

        os.chdir("..")

    def _buildFiles(self) -> None:
        self.files = self.rawFiles

    def build(self) -> None:
        self._loadSource()
        self._buildFiles()
        self._saveBuild()