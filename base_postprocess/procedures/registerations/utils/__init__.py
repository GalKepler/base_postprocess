from base_postprocess.procedures.registerations.utils.register_atlas_steps import (
    collect_requirements,
)

REGISTER_ATLAS_STEPS = [
    {
        "name": "collect_requirements",
        "function": collect_requirements,
        "inputs": ["layout", "subject", "requirements"],
        "outputs": ["result"],
    }
]
