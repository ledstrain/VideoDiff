import numpy as np
import cv2
from skimage.measure import compare_ssim
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    
    # Save the previous frame
    try:
        old_img = img
    except NameError:
       pass
        
    img = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
    try:
        (score, diff) = compare_ssim(img, old_img, full=True, multichannel=True)
    except NameError:
        print "restart loop"
        continue

    diff = (diff * 255).astype("uint8")

    # Display the resulting frame
    cv2.imshow('diff', diff)

    # quit when 'q' is pressed on the image window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
