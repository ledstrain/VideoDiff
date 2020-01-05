import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    
    # Save the previous frame
    try:
        old_img = img
        pb, pg, pr, _ = cv2.split(old_img)    
    except NameError:
       pass
    img = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
    b, g, r, _ = cv2.split(img)
    # Display the resulting frame
    try:
        cv2.imshow('diff', b - pb)
    except NameError:
        pass

    # quit when 'q' is pressed on the image window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()
cap.release()
