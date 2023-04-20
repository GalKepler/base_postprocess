from nipype.interfaces import fsl
from nipype.interfaces.ants import ApplyTransforms

STEPS = {
    "register_to_anatomical_reference": {
        "inputs": {
            "input_image": "input_image",
            "reference_image": "anatomical_reference",
            "transforms": "mni_to_native",
            "output_image": "output_image",
        },
        "args": {"interpolation": "NearestNeighbor"},
        "runner": ApplyTransforms,
    },
    "threshold_probseg": {
        "inputs": {
            "in_file": "gm_probabilistic_segmentation",
            "out_file": "output_image",
        },
        "args": {"thresh": 0.01, "direction": "below"},
        "runner": fsl.Threshold,
    },
    "apply_mask": {
        "inputs": {
            "in_file": "register_to_anatomical_reference_output_image",
            "mask_file": "threshold_probseg_output_image",
            "out_file": "output_image",
        },
        "args": {"output_datatype": "int"},
        "runner": fsl.ApplyMask,
    },
    "register_wholebrain_to_dwi_reference": {
        "inputs": {
            "input_image": "register_to_anatomical_reference_output_image",
            "reference_image": "dwi_reference",
            "output_image": "output_image",
        },
        "args": {"interpolation": "NearestNeighbor", "transforms": "identity"},
        "runner": ApplyTransforms,
        "scope": "session",
    },
    "register_gm_cropped_to_dwi_reference": {
        "inputs": {
            "input_image": "apply_mask_output_image",
            "reference_image": "dwi_reference",
            "output_image": "output_image",
        },
        "args": {"interpolation": "NearestNeighbor", "transforms": "identity"},
        "runner": ApplyTransforms,
        "scope": "session",
    },
}
