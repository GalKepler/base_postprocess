from typing import Union

import logging

from base_postprocess.bids.layout.layout import QSIPREPLayout
from base_postprocess.procedures.tensors.dipy.utils.outputs import OUTPUT_ENTITIES
from base_postprocess.procedures.tensors.dipy.utils.steps import STEPS
from base_postprocess.procedures.tensors.tensor_estimation import TensorEstimation


class DipyTensorEstimation(TensorEstimation):
    """
    A class used to represent a tensor estimation procedure using Dipy.

    Parameters
    ----------
    TensorEstimation : Procedure
        The base class.
    """

    OUTPUTS = OUTPUT_ENTITIES.copy()

    def __init__(
        self,
        layout: QSIPREPLayout,
        name: str = "dipy_tensor_reconstruction",
        steps: dict = STEPS,
        software: str = "dipy",
    ) -> None:
        super().__init__(layout, name, steps, software)

    def execute(
        self, step_name: str, runner, logger: logging.Logger, inputs: dict, args: dict
    ):
        """
        Execute a step.

        Parameters
        ----------
        step_name : str
            The name of the step.
        runner : NiPype runner
            A NiPype runner.
        logger : logging.Logger
            A logger.
        inputs : dict
            The inputs to the step.
        """
        if logger:
            logger.info(f"Running {step_name} with inputs: {inputs} {args}")
            logger.info("Executing: ")
        runner.run(**inputs, **args)
        if logger:
            logger.info(f"Finished running {step_name}")

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
        scope = self.steps.get(step_name).get("scope", "subject")
        if scope == "subject":
            runner = self.steps.get(step_name).get("runner")()
            self.execute(step_name, runner, logger, mapped_inputs, args)
        elif scope == "session":
            for _, session_inputs in mapped_inputs.items():
                runner = self.steps.get(step_name).get("runner")()
                self.execute(step_name, runner, logger, session_inputs, args)
        return outputs

    def run(self, subjects: Union[list, str], force: bool = False) -> dict:
        """
        Run the procedure.

        Parameters
        ----------
        subjects : Union[list, str]
            The subjects to run the procedure on.
        force : bool, optional
            Whether to force the procedure to run, by default False

        Returns
        -------
        dict
            The results of the procedure.
        """
        outputs = {}
        if isinstance(subjects, str):
            subjects = [subjects]
        for subject in subjects:
            logger = self.initiate_logging(subject=subject)
            outputs[subject] = {}
            inputs = self.collect_required_inputs(subject)
            inputs_to_log = (
                f"Running {self.name} on subject {subject} with the following inputs:\n"
            )
            for key, value in inputs.items():
                inputs_to_log += f"{key}: {value}\n"
            logger.info(inputs_to_log)
            for step in self.steps:
                outputs[subject].update(
                    self.run_step(
                        step_name=step, inputs=inputs, force=force, logger=logger
                    )
                )
        return outputs

    @property
    def main_properties(self):
        return {"software": self.software}
