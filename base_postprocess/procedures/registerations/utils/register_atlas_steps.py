# from typing import Union

# from pathlib import Path

# from nipype.interfaces.ants import ApplyTransforms

# from base_postprocess.bids.layout.layout import QSIPREPLayout
# from base_postprocess.procedures.registerations.utils.static import (
#     REGISTER_TO_ANATOMICAL_REFERENCE,
# )


# def register_to_anatomical_reference(
#     layout: QSIPREPLayout,
#     input_image: Union[Path, str],
#     mni_to_native: Union[Path, str],
#     anatomical_reference: Union[Path, str],
#     args: dict = {},
#     output_entities: dict = REGISTER_TO_ANATOMICAL_REFERENCE,
# ):
#     """
#     Register an image to the anatomical reference.

#     Parameters
#     ----------
#     input_image : Union[Path,str]
#         Input image to register.
#     mni_to_native : Union[Path,str]
#         The MNI to native transform.
#     anatomical_reference : Union[Path,str]
#         The anatomical reference image.
#     output_image : Union[Path,str]
#         The output image.
#     args : dict
#         Additional arguments to pass to the ApplyTransforms interface.
#     """
#     output_image = layout.parse_file_entities(anatomical_reference)
#     output_image.update(output_entities)
#     output_image = layout.build_path(output_image, validate=False)
#     runner = ApplyTransforms(
#         input_image=str(input_image),
#         reference_image=str(anatomical_reference),
#         transforms=str(mni_to_native),
#         output_image=str(output_image),
#         **args,
#     )
#     runner.run()
#     return output_image
