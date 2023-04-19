from typing import Union

from pathlib import Path

from base_postprocess.entities.bids_entities import BIDSEntity
from base_postprocess.entities.bids_entities.session.session import Session


class Subject(BIDSEntity):
    """
    A class used to represent a single subject in a BIDS dataset.
    """

    PREFIX = "sub-"

    def __init__(self, path: Union[Path, str]) -> None:
        """
        Initialize a Subject object.

        Parameters
        ----------
        path : Union[Path, str]
            The path to the subject directory.
        """
        super().__init__(path)

    def __repr__(self) -> str:
        """
        Return a string representation of the Subject object.

        Returns
        -------
        str
            The string representation of the Subject object.
        """
        return f"Subject <{self.id}"

    def __str__(self) -> str:
        """
        Return a string representation of the Subject object.

        Returns
        -------
        str
            The string representation of the Subject object.
        """
        return self.id

    def get(self, entities: dict, return_associated: bool = False) -> list[Path]:
        """
        Get a list of files that match the given entities.

        Parameters
        ----------
        entities : dict
            BIDS entities to match.
        return_associated : bool, optional
            Whether to return associated files, by default False

        Returns
        -------
        list[Path]
            A list of files that match the given entities.
        """
        datatype = entities.pop("datatype", None)
        if not datatype:
            raise ValueError("The datatype entity is required.")
        sub_dir = (
            "*"
            if "session" not in entities
            else self.ENTITIES_FORMATS.get("session") + entities.pop("session") + "/*"
        )
        regex = "*"
        for entity, value in self.ENTITIES_FORMATS.items():
            if entity in entities and entity != "extension":
                regex += f"_{value.format(**entities)}"
            elif entity == "extension":
                extension = entities.get(entity, "nii*")
                extension = extension if extension.startswith(".") else f".{extension}"
                regex += extension if not return_associated else ".*"
        print(f"{sub_dir}/{datatype}/{regex}")
        return list(self.path.glob(f"{sub_dir}/{datatype}/{regex}"))

    def get_sessions(self) -> list[Session]:
        return [Session(session) for session in self.path.glob(Session.PREFIX + "*")]

    @property
    def sessions(self) -> list[Session]:
        return self.get_sessions()
