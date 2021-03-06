import cv2
import numpy as np


class VideoDiff:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        self.windowname = None

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.cap.release()

    def process(self, display=True, output_path=None):
        try:
            if display is True:
                cv2.namedWindow(self.windowname, flags=cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)
            if output_path is not None:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            for vimage in self._render(self.cap):
                if display is True:
                    cv2.imshow(self.windowname, vimage)
                if output_path is not None:
                    out.write(vimage)
        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)

    def _render(self, capture_source):
        raise AttributeError('Should be defined in subclass')


class SimpleDither(VideoDiff):
    def __init__(self, source, fill_value=0, state="g"):
        super(SimpleDither, self).__init__(source=source)
        self.windowname = "SimpleDither"
        self.fill_value = fill_value
        self.state = state
        self.framebyframe = False

        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
        }

    @staticmethod
    def __subtraction(fframe, fprevframe, colortoindex, state=None):
        # Zero out all color indexes not specified
        # instead of extracting just the index
        colorindex = colortoindex[state]
        for index in colortoindex.values():
            if index != colorindex:
                fframe[:, :, index] = 0
        frame_difference = fframe - fprevframe
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
        inputkey = cv2.waitKey(1)

        def getkeybind(key):
            if inputkey == ord(key) and self.state != key:
                return True

        # quit when 'q' is pressed on the image window
        if getkeybind('q'):
            print("q: Quit program")
            exit(0)
        elif getkeybind('n'):
            print("n: Switching to normal mode")
            self.state = 'n'
            self.framebyframe = False
        elif getkeybind('r'):
            print("r: Switching to red channel")
            self.state = 'r'
            self.framebyframe = False
        elif getkeybind('g'):
            print("g: Switching to green channel")
            self.state = 'g'
            self.framebyframe = False
        elif getkeybind('b'):
            print("b: Switching to blue channel")
            self.state = 'b'
            self.framebyframe = False
        elif getkeybind('m'):
            print("m: Switching to masking method")
            self.state = 'm'
            self.framebyframe = False

        # No key entered is -1
        if getkeybind('p') or self.framebyframe is True:
            self.framebyframe = True
            while self.framebyframe is True \
                    or inputkey == -1 \
                    or getkeybind('p'):
                inputkey = cv2.waitKey(0)
                if getkeybind('p'):
                    break
                else:
                    self.framebyframe = False

    def _render(self, capture_source):
        prevframe = None
        color = None
        image = None

        while capture_source.isOpened():
            self.__frame_input()

            # Capture frame-by-frame
            ret, frame = capture_source.read()
            if ret is True:
                # Save the previous frame
                if prevframe is not None:
                    prevframe = color
                color = frame

                # First run, save color as prevframe and skip
                # create __mask of image of all changed values
                # Fill changed values to 255
                if prevframe is not None:
                    if self.state in self.colortoindex.keys():
                        image = self.__subtraction(color, prevframe, self.colortoindex, state=self.state)
                    elif self.state == 'm':
                        image = self.__mask(color, prevframe, self.fill_value)
                    elif self.state == 'n':
                        image = color
                else:
                    prevframe = color
                    continue

                yield image

            else:
                # Once video has no more frames
                break
