#: This class is used to represent a single session in a BIDS dataset.

from typing import Union

import datetime
from pathlib import Path


class Session:
    """
    A class used to represent a single session in a BIDS dataset.
    """

    DATE_FORMAT = "%Y%m%d%H%M"  #: The date format used for session IDs.
    PREFIX = "ses-"
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

    def __init__(self, path: Union[str, Path]):
        """
        Initialize a Session object.

        Args:
            path (Union[str, Path]): The path to the session directory.
        """
        self.path = Path(path)

    def __repr__(self) -> str:
        """
        The session ID.

        Returns:
            The session ID.
        """
        return f"Session ({self.path.name})"

    def __str__(self) -> str:
        """
        The session ID.

        Returns:
            The session ID.
        """
        return self.id

    def parse_id(self) -> str:
        """
        Parse the session ID from the path.

        Returns:
            The session ID.
        """
        return self.path.name.replace(self.PREFIX, "")

    def get_datetime(self) -> datetime.datetime:
        """
        Get the date of the session.

        Returns:
            The date of the session.
        """
        return datetime.datetime.strptime(self.parse_id(), self.DATE_FORMAT)

    def get(self, entities: dict, return_associated: bool = False) -> list[Path]:
        """
        Get the path(s) to the file(s) that match the given entities.

        Args:
            entities (dict): The entities to match.
            return_associated (bool, optional): Whether to return associated files.
            Defaults to False.

        Raises:
            ValueError: If the datatype entity is not provided.

        Returns:
            list[Path]: The paths to the file(s) that match the given entities.
        """
        datatype = entities.pop("datatype", None)
        if not datatype:
            raise ValueError("The datatype entity is required.")
        regex = "*"
        for entity, value in self.ENTITIES_FORMATS.items():
            if entity in entities:
                regex += f"_{value.format(**entities)}"
            elif entity == "extension":
                regex += ".nii*" if not return_associated else ".*"
        return list(self.path.glob(f"{datatype}/{regex}"))

    @property
    def id(self) -> str:
        """
        The session ID.

        Returns:
            The session ID.
        """
        return self.parse_id()

    @property
    def date(self) -> datetime.datetime:
        """
        The date of the session.

        Returns:
            The date of the session.
        """
        return self.get_datetime()
