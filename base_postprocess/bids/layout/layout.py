from typing import Union

from pathlib import Path

from bids import BIDSLayout
from bids.layout import add_config_paths

from base_postprocess.bids.config.configurations import CONFIGURATIONS


# Create a new class that is specific to qsiprep's layout
class QSIPREPLayout:
    """
    A class that extends the BIDSLayout class to include
    qsiprep-specific functionality.
    """

    def __init__(self, path: Union[Path, str]) -> None:
        """
        Initialize a QSIPREPLayout object.

        Parameters
        ----------
        path : Union[Path, str]
            The path to the entity directory.
        """
        self.path = Path(path)
        self.add_configurations()
        self.layout = BIDSLayout(self.path, validate=True)

    def add_configurations(self, configurations: dict = CONFIGURATIONS) -> None:
        """
        Add configuration files to the layout.

        Parameters
        ----------
        configurations : dict
            A dictionary containing the configuration files.
        """
        add_config_paths(**configurations)
