# -*- coding: utf-8 -*-
__author__ = 'alex'
from Crypto.Cipher import AES
from Crypto import Random
import random

AES_BLOCK = 16
GRAIN_SIZE = AES_BLOCK * 4


def __plaintext_to_cipher(key, msg):
    msg_str = ''
    for each in msg:
        msg_str += chr(each)
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    return iv + encryptor.encrypt(msg)



def AES_with_given_keys(keys):
    keys_n = len(keys)

    filename = input("请输入文件名:\n")
    fs = open(filename, 'rb')
    fs.seek(0, 0)
    msg = fs.read()
    fs.close()

    print('start encrypting...')

    # deal pad
    x = len(msg) % GRAIN_SIZE
    if x != 0:
        msg_pad = msg + b'1'
        msg_pad += b'0' * (GRAIN_SIZE-x-1)
    else:
        msg_pad = msg + b'1'
        msg_pad += b'0' * (GRAIN_SIZE-1)

    key_sequence = ''
    msg_out = b''

    l = len(msg_pad)
    # for block in msg_pad:
    i = 0
    while i < l:
        index = random.randint(0, keys_n-1)
        key_sequence += (str(index)+'\n')
        key_used = keys[index]
        tmp = __plaintext_to_cipher(key_used, msg_pad[i: i+GRAIN_SIZE])
        # msg_out.append(tmp)
        # msg_out.join(tmp)
        msg_out += tmp
        i += GRAIN_SIZE

    fo = open("key_sequence.txt", 'w')
    fo.write(key_sequence)
    fo.close()

    fo = open("ENC_"+filename, 'wb')
    fo.write(msg_out)
    fo.close()

    print('end encrypting...')