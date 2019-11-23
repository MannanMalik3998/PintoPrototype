import cv2
from mtcnn.mtcnn import MTCNN # import MTCNN

# import facepixellate #try if you want, but its accuracy is not so good 



#provide path to image##################################################################
imagePath='images\\5.jpg'
########################################################################################

detector = MTCNN()#MTCNN initialized

cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')#Haar initialized
# cascade = cv2.CascadeClassifier('haarcascade_licence_plate_rus_16stages.xml')#Haar initialized

def find_and_blur(bw, color): 
    # detect al faces

    ##########################################################
    facesMtcnn = detector.detect_faces(color) #applying mtcnn

     
     #Face detection
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

    ##########################################################
    #Number plate detection
    bw = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

    plates = cascade.detectMultiScale(bw, 1.1, 4)

    for (x, y, w, h) in plates:
        # select the areas where the face was found
        roi_color = color[y:y+h, x:x+w]
        # blur the colored image
        blur = cv2.GaussianBlur(roi_color, (101,101), 0)
        # Insert ROI back into image
        color[y:y+h, x:x+w] = blur    

    ##########################################################

    return color


color = cv2.imread(imagePath)#read image

#cv2.imwrite(imagePath+"Blurred.png",facepixellate.pixellate_face(imagePath, 0)) #accuracy not so good

# detect the face and blur it
blur = find_and_blur(color, color)#blur contains the privacy protected image

############# Now find the hash and sign with tsa #####################

#######################################################################

# display output
cv2.imwrite(imagePath+"Blurred.png",blur)

cv2.imshow("Blurred Photo",blur)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image