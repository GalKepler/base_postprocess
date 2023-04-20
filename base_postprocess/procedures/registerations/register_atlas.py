from typing import Union

from nipype.interfaces import fsl
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

    def register_to_anatomical_reference(
        self, inputs: dict, args: dict = None, force: bool = False
    ) -> dict:
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
        force : bool, optional
            Whether to force the registration, by default False

        Returns
        -------
        dict
            The outputs of the function.
        """
        args = (
            args
            if args is not None
            else self.ARGUMENTS.get("register_to_anatomical_reference").get("args")
        )
        inputs, outputs, outputs_exist = self.update_io_for_step(
            step_name="register_to_anatomical_reference", inputs=inputs
        )
        if not force and all(outputs_exist):
            return outputs
        runner = ApplyTransforms(
            **inputs,
            **args,
        )
        runner.run()
        return outputs

    def threshold_probseg(
        self, inputs: dict, args: dict = None, force: bool = False
    ) -> dict:
        """
        Crop the atlas to the probseg.

        Parameters
        ----------
        inputs : dict
            The inputs to the function.
        output_entities : dict
            The entities to use for the output file.
        args : dict, optional
            The arguments to pass to the function, by default {}
        force : bool, optional
            Whether to force the registration, by default False

        Returns
        -------
        dict
            The outputs of the function.
        """
        args = (
            args
            if args is not None
            else self.ARGUMENTS.get("threshold_probseg").get("args")
        )
        inputs, outputs, outputs_exist = self.update_io_for_step(
            step_name="threshold_probseg", inputs=inputs
        )
        if not force and all(outputs_exist):
            return outputs
        runner = fsl.Threshold(**inputs, **args)
        runner.run()
        return outputs

    def run(self, subjects: Union[list, str], force: bool = False) -> None:
        """
        Run the procedure.

        Parameters
        ----------
        subject : Union[list,str]
            The subject to run the procedure on.
        force : bool, optional
            Whether to force the registration, by default False
        """
        outputs = {}
        if isinstance(subjects, str):
            subjects = [subjects]
        for subject in subjects:
            outputs[subject] = {}
            inputs = self.collect_required_inputs(subject=subject)
            outputs[subject].update(
                self.register_to_anatomical_reference(inputs=inputs)
            )
            inputs.update(outputs[subject])
            outputs[subject].update(self.threshold_probseg(inputs=inputs))
        return outputs
