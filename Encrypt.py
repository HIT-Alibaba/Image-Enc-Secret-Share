# -*- coding: utf-8 -*-
__author__ = 'alex'
from Crypto.Cipher import AES
from Crypto import Random
import random


def plaintext_to_cipher(key, msg):
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    return iv + encryptor.encrypt(msg)



def AES_with_given_keys(keys):
    keys_n = len(keys)

    filename = input("Input file name")
    fs = open(filename, 'r')
    fs.seek(0, 0)
    msg = fs.read()
    fs.close()

    print('start encrypting...')

    # deal pad
    x = len(msg) % 16
    if x != 0:
        msg_pad = msg + '0'*(16 - x)

    key_sequence = ''
    msg_out = ''

    for block in msg_pad:
        index = random.randint(0, keys_n-1)
        key_sequence += str(index)
        key_used = keys[index]
        msg_out += plaintext_to_cipher(key_used, block)

    fo = open("key_sequence.txt", 'w')
    fo.write(key_sequence)
    fo.close()

    fo = open("DEC_"+filename, 'wb')
    fo.write(msg_out)
    fo.close()

    print('end encrypting...')
