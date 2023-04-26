DIFFUSION_TENSOR_OUTPUTS = dict(
    tensor="tensor",
    fa="fa",
    ga="ga",
    rgb="rgb",
    md="md",
    ad="ad",
    rd="rd",
    mode="mode",
    evec="evecs",
    eval="evals",
)
TENSOR_ENTITIES = {"suffix": "dwiref", "resolution": "dwi"}
# Output entities
OUTPUT_ENTITIES = {
    "reconstruct_dti_workflow": {
        f"out_{key}": {
            "reference": "dwi_nifti",
            "entities": {
                **TENSOR_ENTITIES,
                "desc": val,
                "acquisition": "dti",
                "res": "dwi",
                "reconstruction_software": "dipy",
            },
            "include_in_inputs": True,
            "scope": "session",
        }
        for key, val in DIFFUSION_TENSOR_OUTPUTS.items()
    },
}
