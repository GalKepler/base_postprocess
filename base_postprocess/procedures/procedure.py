from pathlib import Path

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

    def update_io_for_step(self, step_name: str, inputs: dict) -> dict:
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
        outputs = {}
        outputs_exist = []
        outputs_config = self.OUTPUTS.get(step_name).copy()
        for output_name, output_values in outputs_config.items():
            entities = output_values.get("entities").copy()
            entities["atlas"] = self.atlas.name
            output_entities = self.layout.parse_file_entities(
                inputs.get(output_values.get("reference"))
            )
            output_entities.update(entities)
            output = self.layout.build_path(output_entities, validate=False)
            outputs[f"{step_name}_{output_name}"] = output
            outputs_exist.append(Path(output).exists())
            include_in_inputs = output_values.get("include_in_inputs", True)
            if include_in_inputs:
                inputs[output_name] = output
        mapped_inputs = {
            key: inputs.get(val)
            for key, val in self.ARGUMENTS.get(step_name).get("inputs").items()
        }
        return mapped_inputs, outputs, outputs_exist

    def run(self) -> None:
        """
        Run the procedure.
        """
