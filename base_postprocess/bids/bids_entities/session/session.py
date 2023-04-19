#: This class is used to represent a single session in a BIDS dataset.

from typing import Union

import datetime
from pathlib import Path

from base_postprocess.bids.bids_entities import BIDSEntity


class Session(BIDSEntity):
    """
    A class used to represent a single session in a BIDS dataset.
    """

    DATE_FORMAT = "%Y%m%d%H%M"  #: The date format used for session IDs.
    PREFIX = "ses-"

    def __init__(self, path: Union[str, Path]):
        """
        Initialize a Session object.

        Parameters
        ----------
        path : Union[str, Path]
            The path to the session directory.
        """
        super().__init__(path=path)

    def __repr__(self) -> str:
        """
        The session ID.

        Returns:
            The session ID.
        """
        return f"Session ({self.id})"

    def __str__(self) -> str:
        """
        The session ID.

        Returns:
            The session ID.
        """
        return self.id

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

        Parameters
        ----------
        entities : dict
            The entities to match.
        return_associated : bool, optional
            Whether to return associated files, by default False.


        Returns
        -------
        list[Path]
            The paths to the file(s) that match the given entities.

        Raises
        ------
        ValueError
            If the datatype entity is not provided.
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
    def date(self) -> datetime.datetime:
        """
        The date of the session.

        Returns:
            The date of the session.
        """
        return self.get_datetime()
