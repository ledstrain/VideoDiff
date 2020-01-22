import cv2
import time
start_time = time.time()


class VideoDiff():
    def __init__(self, source):
        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
        }

        self.cap = cv2.VideoCapture(source)
        self.state = 'b'


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
            print("--- %s seconds ---" % (time.time() - start_time))

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
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(path, fourcc, 20.0, (height, width))

        for vimage in self.__render():
            out.write(vimage)
            print("--- %s seconds ---" % (time.time() - start_time))
        print("done")
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

                # Grab color index set by self state and retrieve from frame
                colorindex = self.colortoindex[self.state]
                color = frame[:, :, colorindex]

                # First run, save color as prevcolor and skip
                # Then compare the two
                if prevcolor is not False:
                    image = color - prevcolor
                else:
                    prevcolor = color
                    continue

                yield image
