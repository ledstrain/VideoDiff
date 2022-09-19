import cv2
import numpy as np


class WindowClass:
    def __init__(self, source):
        self.windowname = None
        self.frame_a = cv2.imread(source[0])
        self.frame_b = cv2.imread(source[1])

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()

    def process(self, display=True):
        try:
            if display is True:
                cv2.namedWindow(self.windowname, flags=cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)
            while True:
                for image in self._render(self.source):
                    if display is True:
                         cv2.imshow(self.windowname, image)
        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)

    def _render(self, capture_source):
        raise AttributeError('Should be defined in subclass')


class ImageDiff(WindowClass):
    def __init__(self, source, fill_value=0, state="g"):
        super(ImageDiff, self).__init__(source=source)
        self.windowname = "ImageDiff"
        self.fill_value = fill_value
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
    def __subtraction(fframe, fprevframe, colortoindex, state=None):
        # Zero out all color indexes not specified
        # instead of extracting just the index
        fframe2 = fframe.copy()
        fprevframe2 = fprevframe.copy()
        colorindex = colortoindex[state]
        for index in colortoindex.values():
            if index != colorindex:
                fframe2[:, :, index] = 0
        frame_difference = fframe2 - fprevframe2
        return frame_difference

    @staticmethod
    def __mask(fframe, fprevframe, fill_value):
        # Mask frame over old frame
        # If element is different, change value to fill_value
        imagemask = np.ma.masked_where(fframe != fprevframe, fframe)
        imagemask.set_fill_value(fill_value)
        masked_frame = imagemask.filled()
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

        elif getkeybind('m'):
            print("m: Switching to masking method")
            self.setState('m')

    def _render(self, source):
        self.__frame_input()
        if self.needRender:
            if self.state in self.colortoindex.keys():
                image = self.__subtraction(self.frame_a, self.frame_b, self.colortoindex, state=self.state)
            elif self.state == 'm':
                image = self.__mask(self.frame_a, self.frame_b, self.fill_value)
            self.needRender = False
            yield image
