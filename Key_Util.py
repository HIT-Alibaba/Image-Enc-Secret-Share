__author__ = 'alex'
import random
from Crypto.Hash import MD5

POW2_128 = 340282366920938463463374607431768211456


def __generate_key(n):
    keys = [''] * n
    factors = [[]] * n
    for i in range(0, n):
        factor = ''
        for j in range(0, i + 1):
            t = random.randint(0, POW2_128)
            factor += str(t)
            factors[i].append(t)
        hasher = MD5.new()
        hasher.update(factor.encode('utf-8'))
        keys[i] = hasher.digest()
    return keys, factors


def key_distribute(n):
    print("distributing keys...")
    keys, factors = __generate_key(n)
    for i in range(0, n):
        fo = open('keystore_' + str(i), 'w')
        buf = ''
        for j in range(0, n):
            t = 0
            for k in range(0, j+1):
                t += factors[j][k] * pow(i+1, k)
                # 当前是给第i个用户生成第j个密钥的碎片，所以将第j个密钥的第k项系数乘该用户的id，i的第几项幂
            buf += str(t)+'\n'
        fo.write(buf)
        fo.close()

    print("finish key distributing!")
    return keys






