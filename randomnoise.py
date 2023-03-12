import numpy as np
import cv2

rng = np.random.default_rng(12345)
frames = []
output_path = "./randomnoise"

def generate_random_frame(width, height):
    frame = rng.integers(256, size=(height, width, 3), dtype=np.uint8)
    return frame

for i in range (0, 500):
    frames.append(generate_random_frame(640, 480))
    output_file = "{output_path}/{frame}.tiff".format(output_path=output_path, frame=i)
    if cv2.haveImageWriter(output_file):
        cv2.imwrite(output_file, frames[i], None) 
        print("Generated frame {i}".format(i=i))
