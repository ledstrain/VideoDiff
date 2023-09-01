import numpy as np

def zero_after_first_index(fframe):
    fframe[:, :, 1:3] = 0
    return fframe

def zero_all_except_last(fframe):
    result = np.zeros(fframe.shape, dtype=np.uint8)
    result[:, :, 2] = fframe[:, :, 2]
    return result

def zero_all_except_middle(fframe):
    fframe[:, :, 0] = 0
    fframe[:, :, 2] = 0
    return fframe

def abs_subtraction(fframe, fprevframe):
    return fframe - fprevframe

def __mask(fframe, fprevframe, fill_value):
        # Mask frame over old frame
        # If element is different, change value to fill_value
    masked_frame = np.uint8(np.where((fframe != fprevframe).any(axis=2, keepdims=True), fill_value, fframe))
    return masked_frame
