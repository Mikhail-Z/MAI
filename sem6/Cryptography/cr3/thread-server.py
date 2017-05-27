import time, threading
from socket import *
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import pickle
import random
import os
import sys
import shutil

def now():
    return time.ctime(time.time())
number = 0

num_of_candidates = 40
valid_electors = list(range(20)) # здесь можно поставить любой список идентификаторов клиентов, которые могут быть избирателями
processed_addresses = []
valid_processed_electors_count = 0
bulletins = dict()

def session_key_decryption(plaintext, filename_end):
    # decryption session key
    privatekey = RSA.importKey(open('bobprivatekey.txt', 'rb').read())
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


def session_key_generation(plaintext, filename_end):
# creation 256 bit session key
	sessionkey = Random.new().read(32)  # 256 bit
	# encryption AES of the message

	iv = Random.new().read(16)  # 128 bit
	obj = AES.new(sessionkey, AES.MODE_CFB, iv)
	ciphertext = iv + obj.encrypt(plaintext)
	# encryption RSA of the session key
	publickey = RSA.importKey(open("client"+filename_end+'/alisapublickey.txt', 'rb').read())
	cipherrsa = PKCS1_OAEP.new(publickey)
	sessionkey = cipherrsa.encrypt(sessionkey)
	f = open("client"+filename_end+'/sessionkey.txt', 'wb')
	f.write(bytes(sessionkey))
	f.close()
	return bytes(ciphertext)


def signature_decoding(plaintext, filename_end):
	# decryption signature
	f = open("client"+filename_end+'/signature.txt', 'rb')
	signature = f.read();
	f.close()
	privatekey = RSA.importKey(open('bobprivatekey.txt', 'rb').read())
	cipherrsa = PKCS1_OAEP.new(privatekey)
	sig = cipherrsa.decrypt(signature[:256])
	sig = sig + cipherrsa.decrypt(signature[256:])
	# signature verification
	publickey = RSA.importKey(open("client"+filename_end+'/alisapublickey.txt', 'rb').read())
	myhash = SHA.new(plaintext)
	signature = PKCS1_v1_5.new(publickey)
	test = signature.verify(myhash, sig)
	if test:
		return True
	else:
		return False


def signature_creation(plaintext, filename_end):
	# creation of signature
	privatekey = RSA.importKey(open('bobprivatekey.txt', 'rb').read())
	myhash = SHA.new(plaintext)
	signature = PKCS1_v1_5.new(privatekey)
	signature = signature.sign(myhash)
	# signature encrypt
	publickey = RSA.importKey(open("client"+filename_end+'/alisapublickey.txt', 'rb').read())
	cipherrsa = PKCS1_OAEP.new(publickey)
	sig = cipherrsa.encrypt(signature[:128])
	sig = sig + cipherrsa.encrypt(signature[128:])
	f = open("client"+filename_end+'/signature.txt', 'wb')
	f.write(bytes(sig))
	f.close()


def text_encoding(reply, filename_end):
	bin_text = bytes(str(reply), 'utf-8')
	signature_creation(bin_text, filename_end)
	return session_key_generation(bin_text, filename_end)


def form_correctness(bulletin):
	i = 0
	n = len(bulletin)
	possible_estimates = ['2', '3', '4', '5', '*']
	if n == num_of_candidates:
		while i < n:
			if bulletin[i] not in possible_estimates:
				break
			i += 1
		if i == n:
			return True
	return False


def firstHandleClient(connection):
	client = None
	estimates = []
	global number
	global valid_processed_electors_count
	filename_end = ""
	while True:
		data = connection.recv(2048)
		data = pickle.loads(data)
		action = data[0]
		if action == '0':
			filename_end = str(number)
			number += 1
			id = data[1]
			if id in valid_electors:
				print("New elector:", id)
				if id not in bulletins:
					valid_processed_electors_count += 1
				os.mkdir("client"+str(filename_end))
				first_message = pickle.dumps(['Yes', str(filename_end)])
				connection.send(first_message)
			else:
				first_message = pickle.dumps(['No'])
				connection.send(first_message)
				connection.close()
				return
		elif action == '2':
			encoded_bulletin = data[1]
			bulletin = session_key_decryption(encoded_bulletin, filename_end)
			if signature_decoding(bulletin, filename_end):
				bulletin = bulletin.decode()
				if form_correctness(bulletin):
					reply = "True"
					voting_confirmation = text_encoding(reply, filename_end)
					connection.send(voting_confirmation)
					for i in range(len(bulletin)):
						if '2' <= bulletin[i] <= '5':
							estimates.append(int(bulletin[i]))
						elif bulletin[i] == '*':
							estimates.append(bulletin[i])
					break
				else:
					reply = "False"
					voting_confirmation = text_encoding(reply, filename_end)
					connection.send(voting_confirmation)
	lock = threading.Lock()
	lock.acquire()
	bulletins[id] = estimates
	lock.release()
	ok = '0'
	while ok != '1':
		ok = connection.recv(2048)
		ok = ok.decode()
		if ok == '1':
			shutil.rmtree("client"+filename_end)
			connection.close()
			return

def get_count_of_votes():
	count_of_votes = []
	for i in range(num_of_candidates):
		count_of_votes.append([0, 0])
		for client in bulletins:
			estimate = bulletins[client][i]
			if estimate != '*':
				count_of_votes[i][0] += estimate
				count_of_votes[i][1] += 1
	return  count_of_votes


eps = 0.01
def get_winner(count_of_votes):
	max_avg = 0
	max_idx = []
	i = 0
	for sum, count in count_of_votes:
		try:
			cur_avg = sum/count
		except ZeroDivisionError:
			cur_avg = 0
		if cur_avg - max_avg > eps:
			max_idx.clear()
			max_idx.append(i)
			max_avg = cur_avg
		elif abs(cur_avg - max_avg) <= eps:
			max_idx.append(i)
		i += 1
	print("winners:", max_idx)
	return max_idx


def dispatcher():
	threads = []
	n = 0
	start = time.time()
	time_out = 20
	#finish = start + num_of_electors*num_of_candidates
	finish = start + time_out
	global valid_processed_electors_count
	while time.time() < finish:
		try:
			connection, address = sockobj.accept()
			sockobj.settimeout(time_out)
		except Exception:
			print("The elections are over!")
			break
		processed_addresses.append(address)
		threads.append(threading.Thread(target=firstHandleClient, args=(connection,)))
		threads[len(threads)-1].start()
	for t in threads:
		t.join()
	count_of_votes = get_count_of_votes()
	print(bulletins)
	winner = get_winner(count_of_votes)


def key_generation():
	# key generation Bob
	privatekey = RSA.generate(2048)
	f = open('bobprivatekey.txt', 'wb')
	f.write(bytes(privatekey.exportKey('PEM')))
	f.close()
	publickey = privatekey.publickey()
	f = open('bobpublickey.txt', 'wb')
	f.write(bytes(publickey.exportKey('PEM')))
	f.close()



if __name__ == "__main__":
	if len(sys.argv) > 1:
		num_of_electors = int(sys.argv[1])
		num_of_candidates = int(sys.argv[2])
		myPort = int(sys.argv[3])
		myHost = "localhost"
		sockobj = socket(AF_INET, SOCK_STREAM) # создать объект сокета TCP
		sockobj.bind((myHost, myPort))
		sockobj.listen(num_of_electors*2)
	else:
		myHost = "localhost"
		myPort = 50005
		sockobj = socket(AF_INET, SOCK_STREAM)
		sockobj.bind((myHost, myPort))
		num_of_electors = 10
		num_of_candidates = 40
		sockobj.listen(num_of_electors*2)

	key_generation()
	dispatcher()
	os.remove("bobprivatekey.txt")
	os.remove("bobpublickey.txt")