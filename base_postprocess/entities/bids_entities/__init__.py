from typing import Union

from pathlib import Path


class BIDSEntity:
    PREFIX = ""

    def __init__(self, path: Union[Path, str]) -> None:
        self.path = Path(path)

    def parse_id(self) -> str:
        return self.path.name.replace(self.PREFIX, "")

    def get(self):
        pass

    @property
    def id(self) -> str:
        return self.parse_id()
