from base_postprocess.procedures.tensors.dipy.dipy_tensor_estimation import (
    DipyTensorEstimation,
)
from base_postprocess.procedures.tensors.mrtrix.mrtrix_tensor_estimation import (
    Mrtrix3TensorEstimation,
)

TENSOR_ESTIMATION_PROCEDURES = {
    "dipy": DipyTensorEstimation,
    "mrtrix3": Mrtrix3TensorEstimation,
}
