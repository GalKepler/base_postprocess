from typing import Union

from pathlib import Path

from bids import BIDSLayout
from bids.exceptions import ConfigError
from bids.layout import add_config_paths

from base_postprocess.bids.config.configurations import CONFIGURATIONS


# Create a new class that is specific to qsiprep's layout
class QSIPREPLayout:
    """
    A class that extends the BIDSLayout class to include
    qsiprep-specific functionality.
    """

    DATABASE_FILE_NAME = "qsiprep_layout.db"

    def __init__(
        self,
        root: Union[Path, str] = None,
        database_path: Union[Path, str] = None,
        reset_database: bool = False,
    ) -> None:
        """
        Initialize a QSIPREPLayout object.

        Parameters
        ----------
        path : Union[Path, str]
            The path to the entity directory.
        """
        self.path = Path(root)
        self.add_configurations()
        self.layout = BIDSLayout(
            self.path,
            validate=False,
            database_path=database_path,
            reset_database=reset_database,
        )

    def add_configurations(self, configurations: dict = CONFIGURATIONS) -> None:
        """
        Add configuration files to the layout.

        Parameters
        ----------
        configurations : dict
            A dictionary containing the configuration files.
        """
        for name, configuration_file in configurations.items():
            try:
                add_config_paths(**{name: configuration_file})
            except ConfigError:
                pass
