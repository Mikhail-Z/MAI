from socket import *
import pickle
import random
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import sys
import os
import argparse
from codecs import encode, decode
serverHost = "localhost"
serverPort = 50003

num_of_candidates = 40
publickey = ""
privatekey = ""

def candidate_choosing(num, manual=False):
    choices = ""
    estimates = ['5', '4', '3', '2', "*"]
    if manual == False:
        for i in range(num):
            choices += str(random.choice(estimates))
    else:
        i = 0
        while i < num:
            choice = str(input("Enter estimate of candidate #{}: ".format(i)))
            if choice in estimates:
                i += 1
                choices += choice
            else:
                print("Wrong estimate. Try again.")
    return choices


def key_generation(filename_end):
    privatekey = RSA.generate(2048)
    f = open("client"+filename_end+'/alisaprivatekey.txt', 'wb')
    f.write(bytes(privatekey.exportKey('PEM')));
    f.close()
    publickey = privatekey.publickey()
    f = open('client'+filename_end+'/alisapublickey.txt', 'wb')
    f.write(bytes(publickey.exportKey('PEM')));
    f.close()


def signature_creation(plaintext, filename_end):
    # creation of signature
    privatekey = RSA.importKey(open("client"+filename_end+'/alisaprivatekey.txt', 'rb').read())
    myhash = SHA.new(plaintext)
    signature = PKCS1_v1_5.new(privatekey)
    signature = signature.sign(myhash)
    # signature encrypt
    publickey = RSA.importKey(open('bobpublickey.txt', 'rb').read())
    cipherrsa = PKCS1_OAEP.new(publickey)
    sig = cipherrsa.encrypt(signature[:128])
    sig = sig + cipherrsa.encrypt(signature[128:])
    f = open('client'+filename_end+'/signature.txt', 'wb')
    f.write(bytes(sig))
    f.close()



def signature_decryption(plaintext, filename_end):
    # decryption signature
    f = open("client"+filename_end+'/signature.txt', 'rb')
    signature = f.read()
    f.close()
    privatekey = RSA.importKey(open("client"+filename_end+'/alisaprivatekey.txt', 'rb').read())
    cipherrsa = PKCS1_OAEP.new(privatekey)
    sig = cipherrsa.decrypt(signature[:256])
    sig = sig + cipherrsa.decrypt(signature[256:])
    # signature verification
    publickey = RSA.importKey(open('bobpublickey.txt', 'rb').read())
    myhash = SHA.new(plaintext)
    signature = PKCS1_v1_5.new(publickey)
    test = signature.verify(myhash, sig)
    if test:
        return True
    else:
        return False


def session_key_generation(plaintext, filename_end):
    # creation 256 bit session key
    sessionkey = Random.new().read(32)  # 256 bit
    # encryption AES of the message

    iv = Random.new().read(16)  # 128 bit
    obj = AES.new(sessionkey, AES.MODE_CFB, iv)
    ciphertext = iv + obj.encrypt(plaintext)
    # encryption RSA of the session key
    publickey = RSA.importKey(open('bobpublickey.txt', 'rb').read())
    cipherrsa = PKCS1_OAEP.new(publickey)
    sessionkey = cipherrsa.encrypt(sessionkey)
    f = open("client"+filename_end+'/sessionkey.txt', 'wb')
    f.write(bytes(sessionkey))
    f.close()
    return ciphertext


def session_key_decryption(plaintext, filename_end):
    # decryption session key
    privatekey = RSA.importKey(open("client"+filename_end+'/alisaprivatekey.txt', 'rb').read())
    cipherrsa = PKCS1_OAEP.new(privatekey)
    f = open("client"+filename_end+'/sessionkey.txt', 'rb')
    sessionkey = f.read(); f.close()
    sessionkey = cipherrsa.decrypt(sessionkey)
    # decryption message
    ciphertext = plaintext
    iv = ciphertext[:16]
    obj = AES.new(sessionkey, AES.MODE_CFB, iv)
    plaintext = obj.decrypt(ciphertext)
    plaintext = plaintext[16:]
    return bytes(plaintext)


def text_encoding(reply, my_file_end):
	bin_text = bytes(str(reply), 'utf-8')
	signature_creation(bin_text, my_file_end)
	return session_key_generation(bin_text, my_file_end)


if __name__=="__main__":

    manual = False
    if len(sys.argv) == 4:
        my_number = int(sys.argv[1])
        num_of_candidates = int(sys.argv[2])
        serverPort = int(sys.argv[3])
    elif len(sys.argv) == 3:
        num_of_candidates = int(sys.argv[1])
        serverPort = int(sys.argv[2])
        manual=True
    if manual:
        my_number = int(input("Enter you id number:"))
    
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((serverHost, serverPort))
    action = "0"
    first_message = pickle.dumps([action, int(my_number)])
    sockobj.send(first_message)

    encoded_filename_end = sockobj.recv(2048)
    encoded_answer = pickle.loads(encoded_filename_end)
    
    if encoded_answer[0] == 'Yes':
        my_file_ending = encoded_answer[1]
        key_generation(my_file_ending)
    else:
        sockobj.close()
        sys.exit()
    my_voice = False
    while my_voice != True:
        estimates_of_candidates = candidate_choosing(num_of_candidates, manual)
        encoded_bulletin = pickle.dumps(['2', text_encoding(estimates_of_candidates, my_file_ending)])
        sockobj.send(encoded_bulletin)
        encoded_voting_confirmation = sockobj.recv(2048)
        voting_confirmation = session_key_decryption(encoded_voting_confirmation, my_file_ending)
        if signature_decryption(voting_confirmation, my_file_ending) and voting_confirmation.decode() == "True":
            sockobj.send(b'1')
            my_voice = True
        else:
            sockobj.send(b'0')
    sockobj.close()
