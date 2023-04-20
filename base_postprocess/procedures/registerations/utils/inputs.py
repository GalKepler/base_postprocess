#: Input and output entities for the registration procedure

# Input entities

REQUIRED_INPUTS = {
    "mni_to_native": {
        "scope": "subject",
        "entities": {
            "from": "MNI152NLin2009cAsym",
            "to": "T1w",
            "suffix": "xfm",
            "mode": "image",
            "extension": "h5",
        },
    },
    "anatomical_reference": {
        "scope": "subject",
        "entities": {
            "desc": "preproc",
            "suffix": "T1w",
            "datatype": "anat",
            "space": None,
            "extension": ".nii.gz",
        },
    },
    "dwi_reference": {
        "scope": "session",
        "entities": {
            "desc": "preproc",
            "datatype": "dwi",
            "suffix": "dwi",
            "space": "T1w",
            "extension": ".nii.gz",
        },
    },
    "gm_probabilistic_segmentation": {
        "scope": "subject",
        "entities": {
            "suffix": "probseg",
            "label": "GM",
            "space": None,
            "extension": ".nii.gz",
        },
    },
}

ARGUMENTS = {
    "register_to_anatomical_reference": {
        "inputs": {
            "input_image": "input_image",
            "reference_image": "anatomical_reference",
            "transforms": "mni_to_native",
            "output_image": "output_image",
        },
        "args": {"interpolation": "NearestNeighbor"},
    },
    "threshold_probseg": {
        "inputs": {
            "in_file": "gm_probabilistic_segmentation",
            "out_file": "output_image",
        },
        "args": {"thresh": 0.01, "direction": "below"},
    },
}
