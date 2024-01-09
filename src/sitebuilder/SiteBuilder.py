from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from os import PathLike

import os
from pathlib import Path

from .Logging import logger
from .MetaFile import MetaFile
from .Template import Template
_logger = logger.getChild("build")

class SiteBuilder():

    def __init__(self, src: str|PathLike, dest: str|PathLike) -> None:
        self.src  = Path(src)
        self.dest = Path(dest)

        self.templates: dict[str, Template]  = {}

        self.meta:      dict[Path, MetaFile] = {}
        self.rawFiles:  dict[Path, str]      = {}
        self.files:     dict[Path, str]      = {}

    def addTemplates(self, path: str|PathLike) -> None:
        path = Path(path)
        for p in path.glob("**/*.html"):
            t = Template(p.stem)
            t.feed(p.read_text())
            self.templates[p.stem] = t

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
        self.dest.mkdir(exist_ok=True)
        os.chdir(self.dest)

        for (path, file) in self.files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                f.write(file)

        os.chdir("..")

    def _buildFiles(self) -> None:
        for p, f in self.rawFiles.items():
            meta = self.meta[p.parent]
            templateKey = meta.getTemplate()
            if templateKey is None:
                self.files[p] = f
                continue

            template = self.templates[templateKey]
            self.files[p] = template.replace(templateKey, f).data

    def build(self) -> None:
        self._loadSource()
        self._buildFiles()
        self._saveBuild()