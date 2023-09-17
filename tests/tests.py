import pytest
from jax import numpy as np
import cv2
from util.video import SimpleDither

class TestVideoDiff:
    def test_red(self):
        tpframes = []
        videoframes = []
        for i in range(2, 6):
            tpframes.append(cv2.imread("testpatterns/r/{i}.tiff".format(i=i)))

        video = SimpleDither('testpatterns/testpattern.mkv', fill_value=255, state='r', framebyframe=False)
        for frame in video._render(video.cap):
            videoframes.append(frame)

        assert np.array_equal(tpframes, videoframes)

    def test_green(self):
        tpframes = []
        videoframes = []
        for i in range(2, 6):
            tpframes.append(cv2.imread("testpatterns/g/{i}.tiff".format(i=i)))

        video = SimpleDither('testpatterns/testpattern.mkv', fill_value=255, state='g', framebyframe=False)
        for frame in video._render(video.cap):
            videoframes.append(frame)
 
        assert np.array_equal(tpframes, videoframes)
    
    def test_blue(self):
        tpframes = []
        videoframes = []
        for i in range(2, 6):
            tpframes.append(cv2.imread("testpatterns/b/{i}.tiff".format(i=i)))

        video = SimpleDither('testpatterns/testpattern.mkv', fill_value=255, state='b', framebyframe=False)
        for frame in video._render(video.cap):
            videoframes.append(frame)
 
        assert np.array_equal(tpframes, videoframes)

    def test_absubtraction(self):
        tpframes = []
        videoframes = []
        for i in range(2, 6):
            tpframes.append(cv2.imread("testpatterns/a/{i}.tiff".format(i=i)))
        
        video = SimpleDither('testpatterns/testpattern.mkv', fill_value=255, state='a', framebyframe=False)
        for frame in video._render(video.cap):
            videoframes.append(frame)
        
        assert np.array_equal(tpframes, videoframes)
