import cv2
from jax import numpy as np
from jax import jit
from numpy import asarray

class WindowClass:
    def __init__(self, source):
        self.windowname = None
        self.frame_a = cv2.imread(source[0])
        self.frame_b = cv2.imread(source[1])

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()

    def process(self, display=True, output_path=None):
        try:
            if display is True:
                cv2.namedWindow(self.windowname, flags=cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)
            while True:
                for image in self._render(self.source):
                    if output_path is not None:
                        if cv2.haveImageWriter(output_path):
                            cv2.imwrite(output_path, image, None)
                    if display:
                        cv2.imshow(self.windowname, asarray(image))
                    else:
                        exit(0)

        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)

    def _render(self, capture_source):
        raise AttributeError('Should be defined in subclass')


class ImageDiff(WindowClass):
    def __init__(self, source, fill_value=0, state="g"):
        super(ImageDiff, self).__init__(source=source)
        self.windowname = "ImageDiff"
        self.fill = np.array([fill_value, fill_value, fill_value], dtype=np.uint8)
        self.state = state
        self.source = source
        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
        }
        self.needRender = True

    def setState(self, key):
        self.state = key
        self.needRender = True

    @staticmethod
    def __subtraction(fframe, fprevframe, state):
        # Zero out all color indexes not specified
        # instead of extracting just the index
        fframe2 = fframe.copy()
        fprevframe2 = fprevframe.copy()
        for i in range(0, 3):
            if i == state:
                continue
            fframe2[:, :, i] = 0
        frame_difference = fframe2 - fprevframe2
        return frame_difference


    @staticmethod
    @jit
    def __abs_subtraction(fframe, fprevframe):
        return fframe - fprevframe

    @staticmethod
    @jit
    def __mask(fframe, fprevframe, fill):
        # Mask frame over old frame
        # If element is different, change value to fill_value
        masked_frame = np.uint8(np.where((fframe != fprevframe).any(axis=2, keepdims=True), fill, fframe))
        return masked_frame

    def __frame_input(self):
        inputkey = cv2.pollKey()

        def getkeybind(key):
            if inputkey == ord(key) and self.state != key:
                return True

        # quit when 'q' is pressed on the image window
        if getkeybind('q'):
            print("q: Quit program")
            exit(0)

        elif getkeybind('r'):
            print("r: Switching to red channel")
            self.setState('r')

        elif getkeybind('g'):
            print("g: Switching to green channel")
            self.setState('g')

        elif getkeybind('b'):
            print("b: Switching to blue channel")
            self.setState('b')

        elif getkeybind('a'):
            print("a: Switching to absolute subtraction method")
            self.setState('a')

        elif getkeybind('m'):
            print("m: Switching to masking method")
            self.setState('m')

        elif getkeybind('i'):
            print("i: Inverting pair of images")
            self.frame_a, self.frame_b = self.frame_b, self.frame_a
            self.needRender = True

        elif getkeybind('1'):
            print("1: Only displaying the first image")
            self.setState(1)

        elif getkeybind('2'):
            print("2: Only displaying the second image")
            self.setState(2)

    def _render(self, source):
        self.__frame_input()
        if self.needRender:
            if self.state in self.colortoindex.keys():
                image = self.__subtraction(self.frame_a, self.frame_b, self.colortoindex[self.state])
            elif self.state == 'a':
                image = self.__abs_subtraction(self.frame_a, self.frame_b)
            elif self.state == 'm':
                image = self.__mask(self.frame_a, self.frame_b, self.fill)
            elif self.state == 1:
                image = self.frame_a
            elif self.state == 2:
                image = self.frame_b

            self.needRender = False
            yield image
