import cv2
from mtcnn.mtcnn import MTCNN # import MTCNN

detector = MTCNN()#MTCNN initialized


cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def find_and_blur(bw, color): 
    # detect al faces
    faces = cascade.detectMultiScale(bw, 1.1, 4)

    facesMtcnn = detector.detect_faces(color) #applying mtcnn

     ##########################################################
    for i in range(len(facesMtcnn)):#Mtcnn
        # get coordinates
        x1, y1, width, height = facesMtcnn[i]['box']#getting bounding box of face
        x2, y2 = x1 + width, y1 + height
        # print("MTCNN")
        # print("x1", x1)
        # print("y1", y1)
        # print("x2", x2)
        # print("y2", y2)
        roi_color = color[y1:y2, x1:x2]
        # blur the colored image
        blur = cv2.GaussianBlur(roi_color, (101,101), 0)
        # Insert ROI back into image
        color[y1:y2, x1:x2] = blur 

        cv2.rectangle(color, (x1,y1), (x2,y2), (0,255,0), 2)#creating rectangle
    
    ##########################################################


    # get the locations of the faces
    # for (x, y, w, h) in faces:
    #     # select the areas where the face was found
    #     roi_color = color[y:y+h, x:x+w]
    #     # blur the colored image
    #     blur = cv2.GaussianBlur(roi_color, (101,101), 0)
    #     # Insert ROI back into image
    #     color[y:y+h, x:x+w] = blur            
    
    # return the blurred image
    return color

# turn camera on

    

video_capture = cv2.VideoCapture(0)

while True:
    # get last recorded frame
    _, color = video_capture.read()
    
    

    
    # transform color -> grayscale
    #bw = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    
    # detect the face and blur it
    blur = find_and_blur(color, color)
    # display output
    cv2.imshow('Video', blur)
    # break if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# turn camera off        
video_capture.release()
# close camera  window
cv2.destroyAllWindows()