from base_postprocess.bids.layout.layout import QSIPREPLayout


class Procedure:
    """
    A general class used to represent a procedure.
    """

    def __init__(self, layout: QSIPREPLayout, name: str) -> None:
        """
        Initialize a Procedure object.

        Parameters
        ----------
        name : str
            The name of the procedure.
        layout : QSIPREPLayout
            The layout on which to apply the procedure.
        """
        self.name = name
        self.layout = layout

    def collect_required_inputs(self, subject: str) -> None:
        """
        Collect the required inputs for the procedure.

        Parameters
        ----------
        subject : str
            The subject to collect the inputs for.
        """
        pass

    def run(self) -> None:
        """
        Run the procedure.
        """
        pass
