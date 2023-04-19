from typing import Any, Union

import pickle
import shutil
from pathlib import Path


class Atlas:
    """
    A class used to represent a parcellation atlas
    """

    CONFIGURED_ATLASES_PATH = Path(__file__).parent / "configured"

    def __init__(
        self, name: str, path: Union[Path, str] = None, load_existing: bool = True
    ):
        """
        Initialize an Atlas object.

        Parameters
        ----------
        name : str
            The name of the atlas.
        """
        self.path = self.get_atlas_path(name=name, path=path)
        self.load_if_existing(name=name, load_existing=load_existing)

    def get_atlas_path(self, name: str, path: Union[Path, str] = None):
        """
        Get the path to the database.

        Parameters
        ----------
        name : str
            The name of the atlas.
        path : Union[Path,str], optional
            The path to the atlas, by default None
        """
        path = Path(path) if path is not None else self.CONFIGURED_ATLASES_PATH / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def load_if_existing(self, name: str, load_existing: bool = True):
        """
        Load an atlas if it exists.

        Parameters
        ----------
        name : str
            The name of the atlas.
        load_existing : bool, optional
            Whether to load an existing atlas, by default True
        """
        path = self.path / f"{name}.obj"
        if path.exists() and load_existing:
            atlas = pickle.load(open(path, "rb"))
            self.__dict__ = atlas.__dict__
        else:
            self.name = name.lower()

    def associate(self, title: str, data: Any):
        """
        Associate a file with the atlas.

        Parameters
        ----------
        title : str
            The title of the file.
        path : str
            The path to the file.
        """
        if isinstance(data, Path) or isinstance(data, str):
            if Path(data).exists():
                data = Path(data).absolute()
                shutil.copy(data, self.path)
                data = self.path / Path(data).name
        setattr(self, title, data)

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
        return data

    def save(self, path: Union[Path, str] = None):
        """
        Save the atlas to a file.

        Parameters
        ----------
        path : Union[Path, str]
            The path to the file.
        """
        if path is None:
            path = self.path / f"{self.name}.obj"
        else:
            path = Path(path)
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @property
    def json(self) -> dict:
        """
        Return the atlas as a JSON string.

        Returns
        -------
        str
            The JSON string.
        """
        return self.to_json()
