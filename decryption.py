# -*- coding: utf-8 -*-
__author__ = 'alex'

import key_util as ku
import numpy as np
from Crypto.Cipher import AES


AES_BLOCK = 16
GRAIN_SIZE = AES_BLOCK * 4
DEC_GRAIN_SIZE = GRAIN_SIZE + 16
BMP_HEAD_LENGTH = 54
KEY_SEQUENCE_FILENAME = "key_sequence.txt"


def __get_pieces():
    n = int(input("请输入参与解密人员人数:\n"))
    pieces = [[] for row in range(n)]
    indexes = [[] for r in range(n)]
    for i in range(0, n):
        # pieces.append([])
        # indexes.append([])
        file_name = input("请输入用户 "+str(i+1)+" 的密钥碎片文件名:\n")
        fi = open(file_name, 'r')
        lines = fi.readlines()
        indexes[i] = int(lines[0])
        fi.close()
        for line in range(1, len(lines)):
            pieces[i].append(int(lines[line]))
    return pieces, indexes, n


def decrypt():
    pieces, indexes, n = __get_pieces()
    keys = ku.key_restore(n, pieces, indexes)
    n_keys = len(keys)
    filename = input("请输入待解密文件名\n")
    fi = open(filename, 'rb')
    fi.seek(0, 0)
    msg = fi.read()
    header = msg[0: BMP_HEAD_LENGTH]
    msg = msg[BMP_HEAD_LENGTH:]
    fi.close()

    print("start decrypting")

    fi = open(KEY_SEQUENCE_FILENAME, 'r')
    lines = fi.readlines()
    fi.close()
    ksq = []
    for each in lines:
        ksq.append(int(each))
    l = len(msg)
    ceiling = l - DEC_GRAIN_SIZE
    i = 0
    msg_out = b''
    while i < ceiling:
        if ksq[i//DEC_GRAIN_SIZE]+1 > n_keys:
            msg_out += msg[i+AES_BLOCK: i+DEC_GRAIN_SIZE]
        else:
            decryptor = AES.new(keys[ksq[i//DEC_GRAIN_SIZE]], AES.MODE_CBC, msg[i: i+AES_BLOCK])
            tmp = decryptor.decrypt(msg[i+AES_BLOCK: i+DEC_GRAIN_SIZE])
            msg_out += tmp
        i += DEC_GRAIN_SIZE

    # deal with pad
    if ksq[i//DEC_GRAIN_SIZE]+1 > n_keys:
        tmp = msg[i+AES_BLOCK: i+DEC_GRAIN_SIZE]
    else:
        decryptor = AES.new(keys[ksq[i//DEC_GRAIN_SIZE]], AES.MODE_CBC, msg[i: i+AES_BLOCK])
        tmp = decryptor.decrypt(msg[i+AES_BLOCK: i+DEC_GRAIN_SIZE])
    x = len(tmp) - 1
    while tmp[x] == b'0':
        x -= 1
    msg_out += tmp[0: x]

    fo = open("DEC"+filename, 'wb')
    fo.write(header + msg_out)
    fo.close()

    print("end decrypting")


if __name__ == '__main__':
    decrypt()
