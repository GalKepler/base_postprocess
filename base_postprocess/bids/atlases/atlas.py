from typing import Union

import pickle
from pathlib import Path


class Atlas:
    """
    A class used to represent a parcellation atlas
    """

    def __init__(self, name: str):
        """
        Initialize an Atlas object.

        Parameters
        ----------
        name : str
            The name of the atlas.
        """
        self.name = name

    def associate_file(self, title: str, path: str):
        """
        Associate a file with the atlas.

        Parameters
        ----------
        title : str
            The title of the file.
        path : str
            The path to the file.
        """
        setattr(self, title, path)

    def to_json(self):
        """
        Convert the atlas to a JSON string.

        Returns
        -------
        str
            The JSON string.
        """
        data = {}
        for key, value in self.__dict__.items():
            data[key] = value

    def save(self, path: Union[Path, str] = None):
        """
        Save the atlas to a file.

        Parameters
        ----------
        path : Union[Path, str]
            The path to the file.
        """
        if path is None:
            path = Path(__file__).parent / "configured" / f"{self.name}.obj"
        else:
            path = Path(path)
        with open(path, "wb") as f:
            pickle.dump(self, f)
