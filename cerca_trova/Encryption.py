from Crypto.Cipher import AES
import hashlib
import base64
BLOCK_SIZE = 32

def decrypt(ciphertext, mode=AES.MODE_ECB):
	key = "ueVbH0RGVHfLBo81/3BqHQ=="
	key = base64.b64decode(key)
	ciphertext = ciphertext.decode("hex")
	encryptor = AES.new(key,mode)
	plaintext = encryptor.decrypt(ciphertext)
	plaintext = pkcs5_unpad(plaintext)
	h = hashlib.new('sha1')
	h.update(plaintext)
	return h.hexdigest()

def encrypt(plaintext, mode=AES.MODE_ECB):
	key = "ueVbH0RGVHfLBo81/3BqHQ=="
	key = base64.b64decode(key)
	cipher = AES.new(key, mode)
	crypted = cipher.encrypt(pkcs5_pad(plaintext))
	crypted = crypted.encode("hex")
	return crypted

def pkcs5_unpad(s):
    return s[0:-ord(s[-1])]
def pkcs5_pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
