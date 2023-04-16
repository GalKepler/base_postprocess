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

    def __init__(self, path: Union[str, Path]):
        """
        Initialize a Session object.

        Args:
            path: Path to the session directory.
        """
        self.path = Path(path)

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
