import cv2
import util.common as common
from jax import numpy as np
from jax import jit
from numpy import asarray
from concurrent.futures import ThreadPoolExecutor, as_completed

class VideoDiff:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        self.windowname = None
        self._tdict = {}
        self._tpe = ThreadPoolExecutor()
        
        if not self.cap.isOpened():
            raise cv2.error("Unable to open capture source: {source}".format(source=source))
            exit(1)

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.cap.release()

    def _save_frame(self, i, frame, output):
        if cv2.haveImageWriter(output):
            return cv2.imwrite(output, frame, None)
    

    def process(self, display=True, output_path=None):
        try:
            if display is True:
                cv2.namedWindow(self.windowname, flags=cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)
            for vimage in self._render(self.cap):
                vimage = asarray(vimage)
                if display is True:
                    cv2.imshow(self.windowname, vimage)
                if output_path is not None:
                    i = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    output_file = "{output_path}/{frame}.tiff".format(output_path=output_path, frame=i)
                    self._tdict.update({self._tpe.submit(self._save_frame, i, vimage, output_file): i})

            for f in as_completed(self._tdict):
                if not f.result():
                    print("Error writing frame {i}".format(i=self._tdict[f]))

        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)

    def _render(self, capture_source):
        raise AttributeError('Should be defined in subclass')


class SimpleDither(VideoDiff):
    def __init__(self, source, fill_value=0, state="g", framebyframe=False):
        super(SimpleDither, self).__init__(source=source)
        self.windowname = "SimpleDither"
        self.fill = np.array([fill_value, fill_value, fill_value], dtype=np.uint8)
        self.state = state
        self.framebyframe = framebyframe
        self.needRender = True

        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
        }

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

            # Save the previous frame
            if prevframe is not None:
                prevframe = frame

            ret, frame = capture_source.read()
            if ret is True:
                # First run, save color as prevframe and skip
                # create __mask of image of all changed values
                # Fill changed values to 255
                if prevframe is not None:
                    if self.state in self.colortoindex.keys():
                        color = common.abs_subtraction(frame, prevframe)
                        if self.state == 'b':
                            color = common.zero_after_first_index(color)
                        elif self.state == 'g':
                            color = common.zero_all_except_middle(color)
                        elif self.state == 'r':
                            color = common.zero_all_except_last(color)
                        image = color
                    elif self.state == 'a':
                        image = common.abs_subtraction(frame, prevframe)
                    elif self.state == 'm':
                        image = common.mask(frame, prevframe, self.fill)
                    elif self.state == 'n':
                        image = frame
                else:
                    prevframe = frame
                    continue
                if self.framebyframe:
                    self.needRender = False
                yield image

            else:
                # Once video has no more frames
                break
