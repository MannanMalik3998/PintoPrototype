import base64
import hashlib
from OpenSSL import crypto

image='out.png'
signaturePath='signature'
CERT_FILE = "selfsigned.crt"

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
        f = open("verificationFolder\\Report.txt", "w")
        f.write("Authenticated")
        f.close()
        print("Authenticated")
    
    except Exception as e:
        f = open("verificationFolder\\Report.txt", "w")
        f.write("Forgery Detected")
        f.close()
        print("Forgery Detected"+e)

detectForgery(CERT_FILE,signaturePath,image)