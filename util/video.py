import cv2
import numpy as np


class VideoDiff:
    def __init__(self, source, fill_value=0):
        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
        }

        self.fill_value = fill_value
        self.cap = cv2.VideoCapture(source)
        self.state = 'g'

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.cap.release()

    @staticmethod
    def getKeyBind(key):
        if cv2.waitKey(1) and 0xFF == ord(key):
            return key

    def show(self):
        windowname = 'diff {}'.format(self.state)
        for vimage in self.__render():
            cv2.imshow(windowname, vimage)

            # quit when 'q' is pressed on the image window
            if self.getKeyBind('q'):
                break
            if self.getKeyBind('r'):
                self.state = 'r'
            if self.getKeyBind('g'):
                self.state = 'g'
            if self.getKeyBind('b'):
                self.state = 'b'

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
        prevcolor = False
        while self.cap.isOpened():
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret is True:
                # Save the previous frame
                if prevcolor is not False:
                    prevcolor = color

                # Zero out all color indexes not specified
                # instead of extracting just the index
                colorindex = self.colortoindex[self.state]
                for index in self.colortoindex.values():
                    if index != colorindex:
                        frame[:, :, index] = 0

                # color = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                color = frame

                # First run, save color as prevcolor and skip
                # create mask of image of all changed values
                # Fill changed values to 255
                if prevcolor is not False:
                    imagemask = np.ma.masked_where(color != prevcolor, color)
                    imagemask.set_fill_value(self.fill_value)
                    image = imagemask.filled()
                else:
                    prevcolor = color
                    continue

                yield image

            else:
                # Once video has no more frames
                break
