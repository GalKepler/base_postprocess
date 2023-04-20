import logging
from pathlib import Path

from base_postprocess.bids.layout.layout import QSIPREPLayout
from base_postprocess.utils.logger import initiate_logger


class Procedure:
    """
    A general class used to represent a procedure.
    """

    REQUIREMENTS = {}
    OUTPUTS = {}
    LOG_DESTINATION_FORMAT = "sub-{subject}/log"
    LOG_NAME_FORMAT = "base_postprocess.{procedure_name}_{procedure_properties}"

    def __init__(self, layout: QSIPREPLayout, name: str, steps: dict = {}) -> None:
        """
        Initialize a Procedure object.

        Parameters
        ----------
        name : str
            The name of the procedure.
        layout : QSIPREPLayout
            The layout on which to apply the procedure.
        steps : dict, optional
            The steps to run, by default {}
        """
        self.name = name
        self.layout = layout
        self.steps = steps

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
            for key, val in self.steps.get(step_name).get("inputs").items()
        }
        return mapped_inputs, outputs, outputs_exist

    def run_step(
        self,
        step_name: str,
        inputs: dict,
        args: dict = None,
        force: bool = False,
        logger: logging.Logger = None,
    ) -> dict:
        """
        Run a step.

        Parameters
        ----------
        step_name : str
            The name of the step.
        inputs : dict
            The inputs to the step.
        force : bool, optional
            Whether to force the step to run, by default False
        Returns
        -------
        dict
            The outputs of the step.
        """
        args = args if args is not None else self.steps.get(step_name).get("args")
        mapped_inputs, outputs, outputs_exist = self.update_io_for_step(
            step_name, inputs
        )
        if not force and all(outputs_exist):
            if logger:
                logger.info(
                    f"Skipping {step_name} as all outputs already exist: {outputs}"
                )
            return outputs
        runner = self.steps.get(step_name).get("runner")
        runner = runner(**mapped_inputs, **args)
        if logger:
            logger.info(f"Running {step_name} with inputs: {mapped_inputs}")
            logger.info("Executing: ")
        runner.run()
        if logger:
            logger.info(f"Finished running {step_name}")
        return outputs

    def initiate_logging(self, subject: str) -> None:
        """
        Initiate logging for the procedure.

        Parameters
        ----------
        subject : str
            The subject to initiate logging for.
        """
        # combine a dictionary of main properties into a single string
        main_properties = self.main_properties
        if main_properties:
            main_properties = "_".join(
                [f"{key}-{val}" for key, val in main_properties.items()]
            )
        else:
            main_properties = ""
        log_destination = Path(self.layout.root) / self.LOG_DESTINATION_FORMAT.format(
            subject=subject,
        )
        log_name = self.LOG_NAME_FORMAT.format(
            procedure_name=self.name,
            procedure_properties=main_properties,
        )
        logger = initiate_logger(log_destination, name=log_name)
        return logger

    def run(self) -> None:
        """
        Run the procedure.
        """

    @property
    def main_properties(self):
        """
        The main properties of the procedure.
        """
        return {}
