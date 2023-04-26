from dipy.workflows.reconst import ReconstDtiFlow

STEPS = {
    "reconstruct_dti_workflow": {
        "inputs": {
            "input_files": "dwi_nifti",
            "bvalues_files": "dwi_bval",
            "bvectors_files": "dwi_bvec",
            "mask_files": "dwi_mask",
        },
        "args": {"fit_method": "NLLS"},
        "runner": ReconstDtiFlow,
        "scope": "session",
    }
}
