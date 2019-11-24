import cv2
from mtcnn.mtcnn import MTCNN # import MTCNN
from OpenSSL import crypto
from socket import gethostname
import cv2
import base64
import hashlib
import os
import sys

############ Initializations ###############

# run python run.py 0 imagePath to blur the sensitive area and sign the image
# run python run.py 1 imagePath to detect forgery in the received image

#sys.argv[0]#path of file
method = sys.argv[1]#parameters
CERT_FILE = "selfsigned.crt"
KEY_FILE = "private.key"

NumberPlateDetectorPath='haarcascade_russian_plate_number.xml'
detector = MTCNN()#MTCNN initialized
cascade = cv2.CascadeClassifier(NumberPlateDetectorPath)#Haar initialized
signaturePath='temp\\signature'

# cascade = cv2.CascadeClassifier(NumberPlateDetectorPath)#Haar initialized

# import facepixellate #try if you want, but its accuracy is not so good 

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

    return color #privacy protected image

def protectPrivacy(img):

    color = cv2.imread(img)#read image

    #cv2.imwrite(imagePath+"Blurred.png",facepixellate.pixellate_face(imagePath, 0)) #accuracy not so good

    # detect the face and blur it
    blur = find_and_blur(color, color)#blur contains the privacy protected image

    # display output
    # cv2.imwrite(imagePath+"Blurred.png",blur)
    cv2.imwrite("temp\\"+"out.png",blur)
    signContent("temp\\"+"out.png")

    cv2.imshow("Blurred Photo",blur)

    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""
   # make a hash object
   h = hashlib.sha1()
   
   # open file for reading in binary mode
   with open(filename,'rb') as file:
       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)
   # return the hex representation of digest
   return h.hexdigest()

def makeCert():#generate a self signed certificate
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)  # generate RSA key-pair

    #Credentials of certificate
    cert = crypto.X509()
    cert.get_subject().C = "PK"
    cert.get_subject().ST = "Karachi"
    cert.get_subject().O = "FAST-NUCES"
    cert.get_subject().OU = "FAST-NUCES"
    cert.get_subject().CN = gethostname()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)  # 10 years expiry date
    cert.set_issuer(cert.get_subject())  # self-sign this certificate

    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    open(CERT_FILE, 'a').close()
    open(KEY_FILE, 'a').close()

    # dumping certificate and keypair on disk
    f = os.open(CERT_FILE,os.O_WRONLY)
    os.write(f, crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    os.close(f)

    f2=os.open(KEY_FILE,os.O_WRONLY)
    os.write(f2, crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    os.close(f2)

def detectForgery(CERT_FILE, signaturePath, received):
    
    try:
        #open certificate
        f = open(CERT_FILE)
        ss_buf = f.read()
        f.close()
        ss_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ss_buf)

        #open the signed content received
        f = open(signaturePath, 'rb')
        sig=f.read()
        f.close()

        # verify the integrity of received image with the certificate and signature
        crypto.verify(ss_cert, sig, hash_file(received), 'sha256')
        print("Authenticated")
    
    except:
        print("Forgery detected")

def signContent(signImagePath):
    try:
        # Now the real world use case; use certificate to verify signature
        f = open(KEY_FILE)
        pv_buf = f.read()
        f.close()
        priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, pv_buf)

        

        
        # # sign and verify PASS
        msg=hash_file(signImagePath)
        sig = crypto.sign(priv_key, msg, 'sha256')#signed the image
        
        open(signaturePath, 'a').close()

        f = open(signaturePath, 'wb')
        f.write(sig)
        f.close()
        
    except:
        print("File path may not be correct")

image = sys.argv[2]
# makeCert() # call to make certificate
if(method=='0'): 
    protectPrivacy(image) # call it to privacy protect the video
elif(method=='1'): 
    detectForgery(CERT_FILE,signaturePath,image) # call it to detect forgery
else:
    print("Wrong input")