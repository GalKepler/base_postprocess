from pathlib import Path

from nipype.interfaces.ants import ApplyTransforms

from base_postprocess.bids.atlases.atlas import Atlas
from base_postprocess.bids.layout.layout import QSIPREPLayout
from base_postprocess.procedures.procedure import Procedure

# from base_postprocess.procedures.registerations.utils import REGISTER_ATLAS_STEPS
from base_postprocess.procedures.registerations.utils.inputs import (
    ARGUMENTS,
    REQUIRED_INPUTS,
)
from base_postprocess.procedures.registerations.utils.outputs import OUTPUT_ENTITIES


class RegisterAtlas(Procedure):
    """
    A class used to represent a registration procedure.
    """

    REQUIREMENTS = REQUIRED_INPUTS
    OUTPUTS = OUTPUT_ENTITIES
    ARGUMENTS = ARGUMENTS

    def __init__(
        self,
        atlas: Atlas,
        layout: QSIPREPLayout,
        name: str = "register_atlas",
        # steps: list = REGISTER_ATLAS_STEPS,
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
        # self.steps = steps
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

    def register_to_anatomical_reference(self, inputs: dict, args: dict = None) -> Path:
        """
        Register the atlas to the anatomical reference.

        Parameters
        ----------
        inputs : dict
            The inputs to the function.
        output_entities : dict
            The entities to use for the output file.
        args : dict, optional
            The arguments to pass to the function, by default {}

        Returns
        -------
        Path
            The path to the output file.
        """
        args = (
            args
            if args is not None
            else self.ARGUMENTS.get("register_to_anatomical_reference").get("args")
        )
        inputs, outputs = self.update_inputs_for_step(
            step_name="register_to_anatomical_reference", inputs=inputs
        )
        runner = ApplyTransforms(
            **inputs,
            **args,
        )
        runner.run()
        return outputs

    def run(self, subject: str) -> None:
        """
        Run the procedure.
        """
        for step in self.steps:
            step["function"](**{key: step[key] for key in step["inputs"]})
