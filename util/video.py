import cv2
import numpy as np


class VideoDiff:
    def __init__(self, source, fill_value=0, dither_method="diff", state="g"):
        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
        }

        self.fill_value = fill_value
        self.cap = cv2.VideoCapture(source)
        self.state = state
        self.dither_method = dither_method

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.cap.release()

    @staticmethod
    def getKeyBind(key):
        if cv2.waitKey(1) == ord(key):
            return key

    def show(self):
        try:
            for vimage in self.__render():
                # if self.dither_method == "diff":
                #     windowname = 'Diff {}'.format(self.state.upper())
                # elif self.dither_method == "mask":
                #     windowname = "Masked"
                windowname = "Dither"
                cv2.imshow(windowname, vimage)

                # quit when 'q' is pressed on the image window
                if self.getKeyBind('q'):
                    print("q: Quit program")
                    break
                if self.getKeyBind('r') and self.state != 'r':
                    print("r: Switching to red channel")
                    self.state = 'r'
                if self.getKeyBind('g') and self.state != 'g':
                    print("g: Switching to green channel")
                    self.state = 'g'
                if self.getKeyBind('b') and self.state != 'b':
                    print("b: Switching to blue channel")
                    self.state = 'b'
                if self.getKeyBind('m') and self.state != 'm':
                    print("m: Switching to masking method")
                    self.state = 'm'

        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)

    def save(self, path):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(path, fourcc, fps, (width, height))

        for vimage in self.__render():
            out.write(vimage)
        out.release()

    def __render(self):
        prevframe = False
        color = None

        def subtraction(fframe, fprevframe, colortoindex):
            # Zero out all color indexes not specified
            # instead of extracting just the index
            colorindex = colortoindex[self.state]
            for index in colortoindex.values():
                if index != colorindex:
                    frame[:, :, index] = 0
            frame_difference = fframe - fprevframe
            return frame_difference

        def mask(fframe, fprevframe, fill_value):
            # Mask frame over old frame
            # If element is different, change value to fill_value
            imagemask = np.ma.masked_where(fframe != fprevframe, fframe)
            imagemask.set_fill_value(fill_value)
            masked_frame = imagemask.filled()
            return masked_frame

        while self.cap.isOpened():
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret is True:
                # Save the previous frame
                if prevframe is not False:
                    prevframe = color
                color = frame

                # First run, save color as prevframe and skip
                # create mask of image of all changed values
                # Fill changed values to 255
                if prevframe is not False:
                    if self.state in self.colortoindex.keys():
                        image = subtraction(color, prevframe, self.colortoindex)
                    elif self.state == 'm':
                        image = mask(color, prevframe, self.fill_value)
                else:
                    prevframe = color
                    continue

                yield image

            else:
                # Once video has no more frames
                break
