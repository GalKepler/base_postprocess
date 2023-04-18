from typing import Union

from pathlib import Path


class BIDSEntity:
    PREFIX = ""
    ENTITIES_FORMATS = {
        "direction": "dir-{direction}",
        "space": "space-{space}",
        "resolution": "res-{resolution}",
        "label": "label-{label}",
        "atlas": "atlas-{atlas}",
        "description": "desc-{description}",
        "suffix": "{suffix}",
        "extension": ".{extension}",
    }

    def __init__(self, path: Union[Path, str]) -> None:
        self.path = Path(path)

    def parse_id(self) -> str:
        return self.path.name.replace(self.PREFIX, "")

    def get(self):
        pass

    @property
    def id(self) -> str:
        return self.parse_id()
