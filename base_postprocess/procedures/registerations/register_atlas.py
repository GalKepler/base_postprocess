from base_postprocess.bids.atlases.atlas import Atlas
from base_postprocess.bids.layout.layout import QSIPREPLayout
from base_postprocess.procedures.procedure import Procedure
from base_postprocess.procedures.registerations.utils import REGISTER_ATLAS_STEPS


class RegisterAtlas(Procedure):
    """
    A class used to represent a registration procedure.
    """

    def __init__(
        self,
        atlas: Atlas,
        layout: QSIPREPLayout,
        name: str = "register_atlas",
        steps: list = REGISTER_ATLAS_STEPS,
    ) -> None:
        """
        Initialize a RegisterAtlas object.

        Parameters
        ----------
        atlas : Atlas
            The atlas to register.
        layout : QSIPREPLayout
            The layout on which to apply the procedure.
        name : str, optional
            The name of the procedure, by default "register_atlas"
        steps : list, optional
            The steps to run, by default REGISTER_ATLAS_STEPS
        """
        super().__init__(name, layout)
        self.atlas = atlas
        self.steps = steps

    def collect_required_inputs(self, subject: str) -> None:
        """
        Collect the required inputs for the procedure.

        Parameters
        ----------
        subject : str
            The subject to collect the inputs for.
        """

    def run(self, subject: str) -> None:
        """
        Run the procedure.
        """
        for step in self.steps:
            step["function"](**{key: step[key] for key in step["inputs"]})
