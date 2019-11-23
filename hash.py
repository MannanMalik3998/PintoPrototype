
imagePath='images\\1.pngPixelated.png'
imagePath2='images\\1.pngPixelated2.png'


# importing the hashlib module
import hashlib
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
message = hash_file(imagePath)
print(message)
print(hash_file(imagePath)==hash_file(imagePath))

import OpenSSL
from OpenSSL import crypto
import base64
key_file = open("C:\my.pem", "r")
key = key_file.read()
key_file.close()
password = "password of prk"

if key.startswith('-----BEGIN '):
    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key, password)
else:
    pkey = crypto.load_pkcs12(key, password).get_privatekey()
print pkey
data = "data"
sign = OpenSSL.crypto.sign(pkey, data, "sha256") 
print sign

data_base64 = base64.b64encode(sign)
print data_base64