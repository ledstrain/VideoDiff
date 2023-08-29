import jax
from jax import numpy as np

@jax.jit
def zero_after_first_index(fframe):
    fframe = fframe.at[:, :, 1:3].set(0)
    return fframe

@jax.jit
def zero_middle(fframe):
    result = np.zeros(fframe.shape, dtype=np.uint8)
    result = result.at[:, :, 1].set(fframe[:, :, 1])
    return result

@jax.jit
def zero_all_except_last(fframe):
    fframe = fframe.at[:, :, 0:2].set(0)
    return fframe

@jax.jit
def abs_subtraction(fframe, fprevframe):
    return fframe - fprevframe

@jax.jit
def mask(fframe, fprevframe, fill):
    masked_frame = np.uint8(np.where((fframe != fprevframe).any(axis=2, keepdims=True), fill, fframe))
    return masked_frame
