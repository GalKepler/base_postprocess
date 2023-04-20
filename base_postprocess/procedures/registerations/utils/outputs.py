# Output entities
OUTPUT_ENTITIES = {
    "register_to_anatomical_reference": {
        "output_image": {
            "reference": "anatomical_reference",
            "entities": {
                "space": "T1w",
                "suffix": "dseg",
                "desc": "",
                "res": "T1w",
                "label": "WholeBrain",
            },
            "include_in_inputs": True,
        },
    },
    "threshold_probseg": {
        "output_image": {
            "reference": "gm_probabilistic_segmentation",
            "entities": {
                "suffix": "mask",
            },
            "include_in_inputs": True,
        },
    },
    "apply_mask": {
        "output_image": {
            "reference": "register_to_anatomical_reference_output_image",
            "entities": {
                "label": "GM",
            },
            "include_in_inputs": True,
        },
    },
    "register_wholebrain_to_dwi_reference": {
        "output_image": {
            "reference": "dwi_reference",
            "entities": {
                "space": "T1w",
                "suffix": "dseg",
                "desc": "",
                "res": "T1w",
                "label": "WholeBrain",
            },
            "include_in_inputs": True,
        },
    },
}
