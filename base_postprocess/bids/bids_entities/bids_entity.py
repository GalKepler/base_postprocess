from typing import Union

from pathlib import Path


class BIDSEntity:
    """
    A class used to represent a single BIDS entity.
    """

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
        """
        Initialize a BIDSEntity object.

        Parameters
        ----------
        path : Union[Path, str]
            The path to the entity directory.
        """
        self.path = Path(path)

    def parse_id(self) -> str:
        """
        Parse the entity ID from the path.

        Returns
        -------
        str
            The entity ID.
        """
        return self.path.name.replace(self.PREFIX, "")

    def get(self):
        """
        Get a list of files that match the given entities.
        """
        pass

    @property
    def id(self) -> str:
        """
        Return the entity ID.

        Returns
        -------
        str
            The entity ID.
        """
        return self.parse_id()
