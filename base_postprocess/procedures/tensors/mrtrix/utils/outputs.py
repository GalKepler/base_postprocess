DIFFUSION_TENSOR_OUTPUTS = dict(
    adc="md",
    fa="fa",
    ad="ad",
    rd="rd",
    cl="cl",
    cp="cp",
    cs="cs",
    evec="evecs",
    eval="evals",
    tensor="tensor",
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
                "reconstruction_software": "mrtrix",
            },
            "include_in_inputs": True,
            "scope": "session",
        }
        for key, val in DIFFUSION_TENSOR_OUTPUTS.items()
    },
}
