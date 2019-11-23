import cv2
from mtcnn.mtcnn import MTCNN # import MTCNN

detector = MTCNN()#MTCNN initialized

def find_and_blur(bw, color): 
    # detect al faces

    facesMtcnn = detector.detect_faces(color) #applying mtcnn

     ##########################################################
    for i in range(len(facesMtcnn)):#Mtcnn
        # get coordinates
        x1, y1, width, height = facesMtcnn[i]['box']#getting bounding box of face
        x2, y2 = x1 + width, y1 + height
        roi_color = color[y1:y2, x1:x2]
        # blur the colored image
        blur = cv2.GaussianBlur(roi_color, (101,101), 0)
        # Insert ROI back into image
        color[y1:y2, x1:x2] = blur 

    ##########################################################

    return color

#provide path to image
imagePath='C:\\Users\\hp\\Desktop\\3.png'

color = cv2.imread(imagePath)#read image


# detect the face and blur it
blur = find_and_blur(color, color)

# display output
cv2.imwrite(imagePath+"Pixelated.png",blur)

cv2.imshow("Blurred Photo",blur)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image