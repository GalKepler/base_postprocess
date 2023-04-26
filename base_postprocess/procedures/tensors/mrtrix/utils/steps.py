from base_postprocess.procedures.tensors.mrtrix.utils.workflows.reconst import (
    ReconstDtiFlow,
)

STEPS = {
    "reconstruct_dti_workflow": {
        "inputs": {
            "in_file": "dwi_nifti",
            "grad": "dwi_grad",
            "mask_file": "dwi_mask",
        },
        "args": {},
        "runner": ReconstDtiFlow,
        "scope": "session",
    }
}
