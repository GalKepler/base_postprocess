from typing import Union

from pathlib import Path

from base_postprocess.entities.bids_entities import BIDSEntity
from base_postprocess.entities.bids_entities.session.session import Session


class Subject(BIDSEntity):
    """
    A class used to represent a single subject in a BIDS dataset.
    """

    PREFIX = "sub-"

    def __init__(self, path: Union[str, Path]) -> None:
        super().__init__(path=path)

    def __repr__(self) -> str:
        return f"Subject <{self.id}"

    def __str__(self) -> str:
        return self.id

    def get(self, entities: dict, return_associated: bool = False) -> list[Path]:
        """_summary_

        Parameters
        ----------
        entities : dict
            _description_
        return_associated : bool, optional
            _description_, by default False

        Returns
        -------
        list[Path]
            _description_
        """
        datatype = entities.pop("datatype", None)
        if not datatype:
            raise ValueError("The datatype entity is required.")
        regex = (
            "*"
            if "session" not in entities
            else self.ENTITIES_FORMATS.get("session") + entities.pop("session") + "/*"
        )
        for entity, value in self.ENTITIES_FORMATS.items():
            if entity in entities:
                regex += f"_{value.format(**entities)}"
            elif entity == "extension":
                regex += ".nii*" if not return_associated else ".*"
        return list(self.path.glob(f"{datatype}/{regex}"))

    def get_sessions(self) -> list[Session]:
        return [Session(session) for session in self.path.glob(Session.PREFIX + "*")]

    @property
    def sessions(self) -> list[Session]:
        return self.get_sessions()
