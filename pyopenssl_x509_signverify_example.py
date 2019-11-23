from OpenSSL import crypto
from socket import gethostname
import cv2
import base64

CERT_FILE = "selfsigned.crt"
KEY_FILE = "private.key"
imagePath='images\\1.pngPixelated.png'
imagePath2='images\\1.pngPixelated2.png'

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

def makeCert():#generate a self signed certificate
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)  # generate RSA key-pair


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

   

    # pass certificate around, but of course keep private.key

    import os

    open(CERT_FILE, 'a').close()
    open(KEY_FILE, 'a').close()

    f = os.open(CERT_FILE,os.O_WRONLY)
    os.write(f, crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    os.close(f)

    f2=os.open(KEY_FILE,os.O_WRONLY)
    os.write(f2, crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    os.close(f2)


# makeCert() # call to make certificate

# Now the real world use case; use certificate to verify signature
f = open(KEY_FILE)
pv_buf = f.read()
f.close()
priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, pv_buf)

#open certificate
f = open(CERT_FILE)
ss_buf = f.read()
f.close()
ss_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ss_buf)

try:
    # # sign and verify PASS
    msg=hash_file(imagePath)
    sig = crypto.sign(priv_key, msg, 'sha256')
    crypto.verify(ss_cert, sig, hash_file(imagePath), 'sha256')
    print("Successfully signed")
    data_base64 = base64.b64encode(sig)
    print(data_base64)

except:
    print("Signing failed due to corrupted/forged data")
