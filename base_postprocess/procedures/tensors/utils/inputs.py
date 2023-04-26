#: Input and output entities for the registration procedure

# Input entities

REQUIRED_INPUTS = {
    "dwi_nifti": {
        "scope": "session",
        "entities": {
            "desc": "preproc",
            "datatype": "dwi",
            "suffix": "dwi",
            "space": "T1w",
            "extension": ".nii.gz",
        },
    },
    "dwi_bval": {
        "scope": "session",
        "entities": {
            "desc": "preproc",
            "datatype": "dwi",
            "suffix": "dwi",
            "space": "T1w",
            "extension": ".bval",
        },
    },
    "dwi_bvec": {
        "scope": "session",
        "entities": {
            "desc": "preproc",
            "datatype": "dwi",
            "suffix": "dwi",
            "space": "T1w",
            "extension": ".bvec",
        },
    },
    "dwi_grad": {
        "scope": "session",
        "entities": {
            "desc": "preproc",
            "datatype": "dwi",
            "suffix": "dwi",
            "space": "T1w",
            "extension": ".b",
        },
    },
    "dwi_mask": {
        "scope": "session",
        "entities": {
            "desc": "brain",
            "datatype": "dwi",
            "suffix": "mask",
            "space": "T1w",
            "extension": ".nii.gz",
        },
    },
}
