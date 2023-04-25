from typing import Union

from base_postprocess.bids.atlases.atlas import Atlas
from base_postprocess.bids.layout.layout import QSIPREPLayout
from base_postprocess.procedures.procedure import Procedure

# from base_postprocess.procedures.registerations.utils import REGISTER_ATLAS_STEPS
from base_postprocess.procedures.registerations.utils.inputs import REQUIRED_INPUTS
from base_postprocess.procedures.registerations.utils.outputs import OUTPUT_ENTITIES
from base_postprocess.procedures.registerations.utils.steps import STEPS


class RegisterAtlas(Procedure):
    """
    A class used to represent a registration procedure.
    """

    REQUIREMENTS = REQUIRED_INPUTS
    OUTPUTS = OUTPUT_ENTITIES

    def __init__(
        self,
        atlas: Atlas,
        layout: QSIPREPLayout,
        name: str = "register_atlas",
        steps: dict = STEPS,
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
        super().__init__(name=name, layout=layout)
        self.atlas = atlas
        self.steps = steps
        self.OUTPUTS["atlas"] = self.atlas.name

    def collect_required_inputs(self, subject: str) -> None:
        """
        Collect the required inputs for the procedure.

        Parameters
        ----------
        subject : str
            The subject to collect the inputs for.
        """
        result = {"input_image": self.atlas.atlas_nifti_file}
        for key, description in self.REQUIREMENTS.items():
            scope = description["scope"]
            entities = description["entities"].copy()
            entities["subject"] = subject
            if scope == "session":
                result[key] = {}
                for session in self.layout.get_sessions(subject=subject):
                    entities["session"] = session
                    value = self.layout.get_file_by_entities(entities)
                    result[key][session] = value
            elif scope == "subject":
                value = self.layout.get_file_by_entities(entities)
                result[key] = value
        return result

    def run(self, subjects: Union[list, str], force: bool = False) -> dict:
        """
        Run the procedure.

        Parameters
        ----------
        subject : Union[list,str]
            The subject to run the procedure on.
        force : bool, optional
            Whether to force the registration, by default False

        Returns
        -------
        dict
            The outputs of the procedure.
        """
        outputs = {}
        if isinstance(subjects, str):
            subjects = [subjects]
        for subject in subjects:
            logger = self.initiate_logging(subject=subject)
            outputs[subject] = {}
            inputs = self.collect_required_inputs(subject=subject)
            inputs_to_log = (
                f"Running {self.name} on subject {subject} with the following inputs:\n"
            )
            for key, value in inputs.items():
                inputs_to_log += f"{key}: {value}\n"
            logger.info(inputs_to_log)
            for step in self.steps:
                outputs[subject].update(
                    self.run_step(
                        step_name=step,
                        inputs=inputs,
                        force=force,
                        logger=logger,
                    )
                )
                inputs.update(outputs[subject])
        return outputs

    @property
    def main_properties(self):
        """
        Return the main properties of the procedure.
        """
        return {"atlas": self.atlas.name}
