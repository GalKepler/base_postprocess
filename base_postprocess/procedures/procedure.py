from base_postprocess.bids.layout.layout import QSIPREPLayout


class Procedure:
    """
    A general class used to represent a procedure.
    """

    REQUIREMENTS = {}
    OUTPUTS = {}
    ARGUMENTS = {}

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

    def build_output_dictionary(self, subject: str) -> None:
        """
        Build the output dictionary for the procedure.

        Parameters
        ----------
        subject : str
            The subject to build the output dictionary for.
        """
        pass

    def update_inputs_for_step(self, step_name: str, inputs: dict) -> dict:
        """
        Update the inputs for a step.

        Parameters
        ----------
        step_name : str
            The name of the step.
        inputs : dict
            The inputs to the step.

        Returns
        -------
        dict
            The updated inputs.
        """
        outputs = self.OUTPUTS.get(step_name).copy()
        entities = outputs.get("entities").copy()
        entities["atlas"] = self.atlas.name
        output_entities = self.layout.parse_file_entities(
            inputs.get(outputs.get("reference"))
        )
        output_entities.update(entities)
        outputs = {
            outputs.get("output_name"): self.layout.build_path(
                output_entities, validate=False
            )
        }
        inputs.update(outputs)
        mapped_inputs = {
            key: inputs.get(val)
            for key, val in self.ARGUMENTS.get(step_name).get("inputs").items()
        }
        return mapped_inputs, outputs

    def run(self) -> None:
        """
        Run the procedure.
        """
