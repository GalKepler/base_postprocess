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
}
