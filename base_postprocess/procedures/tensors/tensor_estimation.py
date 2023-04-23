from base_postprocess.bids.layout.layout import QSIPREPLayout
from base_postprocess.procedures.procedure import Procedure
from base_postprocess.procedures.tensors.utils.inputs import REQUIRED_INPUTS
from base_postprocess.procedures.tensors.utils.utils import parse_inputs_to_sessions


class TensorEstimation(Procedure):
    """
    A class used to represent a tensor estimation procedure.
    """

    REQUIREMENTS = REQUIRED_INPUTS.copy()

    def __init__(
        self, layout: QSIPREPLayout, name: str, steps: dict = {}, software: str = ""
    ) -> None:
        super().__init__(layout, name, steps)
        self.software = software

    def collect_required_inputs_by_session(self, subject: str) -> dict:
        """
        Collect the required inputs for the procedure.

        Parameters
        ----------
        subject : str
            The subject to collect the inputs for.
        """
        inputs = self.collect_required_inputs(subject)
        return parse_inputs_to_sessions(inputs)
