import cv2
import numpy as np
import util.common as common

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

            for vimage in self._render(self.cap):
                if display is True:
                    cv2.imshow(self.windowname, vimage)
                if output_path is not None:
                    frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    output_file = "{output_path}/{frame}.tiff".format(output_path=output_path, frame=frame)
                    if cv2.haveImageWriter(output_file):
                       cv2.imwrite(output_file, vimage, None) 
        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)

    def _render(self, capture_source):
        raise AttributeError('Should be defined in subclass')


class SimpleDither(VideoDiff):
    def __init__(self, source, fill_value=0, state="g", framebyframe=False):
        super(SimpleDither, self).__init__(source=source)
        self.windowname = "SimpleDither"
        self.fill_value = fill_value
        self.state = state
        self.framebyframe = framebyframe
        self.needRender = True

        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
            "a": 3, # absolute (not alpha, used internally)
        }

    @staticmethod
    def __subtraction(fframe, fprevframe, colortoindex, state=None):
        # Zero out all color indexes not specified
        # instead of extracting just the index
        colorindex = colortoindex[state]
        for index in colortoindex.values():
            if state == 'a':
                return fprevframe - fframe
            if index != colorindex and index < 3:
                fframe[:, :, index] = 0
        frame_difference = fframe - fprevframe
        return frame_difference

    @staticmethod
    def __mask(fframe, fprevframe, fill_value):
        # Mask frame over old frame
        # If element is different, change value to fill_value
        masked_frame = np.uint8(np.where((fframe != fprevframe).any(axis=2, keepdims=True), [fill_value,fill_value,fill_value], fframe))
        return masked_frame

    def setState(self, key):
        self.state = key
        self.needRender = True

    def __frame_input(self):
        inputkey = cv2.pollKey()

        def getkeybind(key):
            if inputkey == ord(key) and self.state != key:
                return True

        # quit when 'q' is pressed on the image window
        if getkeybind('q'):
            print("q: Quit program")
            exit(0)

        elif getkeybind('n'):
            print("n: Switching to normal mode")
            self.setState('n')

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

        elif getkeybind('p'):
            if not self.framebyframe:
                print("p: Switching to frame-to-frame mode")
                self.framebyframe = True
            self.needRender = True

        elif getkeybind('c'):
            if self.framebyframe:
                print("c: Switching back to normal playback mode")
                self.framebyframe = False
                self.needRender = True

    def _render(self, capture_source):
        prevframe = None
        color = None
        image = None

        while capture_source.isOpened():
            self.__frame_input()
            if self.framebyframe and not self.needRender:
                continue

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
                        if self.state == 'b':
                            color = common.zero_after_first_index(color)
                        elif self.state == 'g':
                            color = common.zero_middle(color)
                        elif self.state == 'r':
                            color = common.zero_all_except_last(color)
                        image = common.abs_subtraction(color, prevframe)
                    elif self.state == 'm':
                        image = self.__mask(color, prevframe, self.fill_value)
                    elif self.state == 'n':
                        image = color
                else:
                    prevframe = color
                    continue
                if self.framebyframe:
                    self.needRender = False
                yield image

            else:
                # Once video has no more frames
                break
