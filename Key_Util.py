# -*- coding: utf-8 -*-

__author__ = 'alex'
import random
from Crypto.Hash import MD5
import numpy as np

POW2_20 = 1048576


def __generate_key(n):
    """利用<i><b>拉格朗日插值法</i></b>生成密钥，初始密钥为低阶系数到高阶系数的拼接字符串，根据这些初始密钥MD5散列出AES密钥"""

    keys = [''] * n
    factors = [[]] * n
    hasher = MD5.new()
    for i in range(0, n):
        factor = ''
        for j in range(0, i + 1):
            t = random.randint(0, POW2_20)
            factor += str(t)
            factors[i].append(t)
        print("系数拼凑:")
        print(factor)
        print("被哈希的:")
        print(factor.encode('utf-8'))
        hasher.update(factor.encode('utf-8'))
        keys[i] = hasher.digest()
    print("生成user keys:")
    print(keys)
    return keys, factors


def key_distribute(n = 10):
    """为每个用户生成密钥并分发到对应文件里。文件第一行记录碎片总数(即用户总数)，下面依次记录每个密钥的碎片"""
    print("distributing keys...")
    keys, factors = __generate_key(n)
    for i in range(0, n):
        fo = open('keystore_' + str(i), 'w')
        buf = str(i)+'\n'
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

def key_restore(n, pieces):
    """根据碎片恢复密钥。对于给定的n*N的pieces,只能恢复前n个密钥"""

    # prepare
    viriables = [[]] * n
    keys = []
    for i in range(0, n):
        viriables[i].append(1)
        for j in range(1, n):
            viriables[i].append(viriables[i][j-1] * i)

    pieces_a = np.array(pieces)
    view_holder = [False] * len(pieces[0])
    last_curse = 0
    hasher = MD5.new()
    for i in range(0, n):
        view_holder[last_curse] = False
        view_holder[i] = True
        cup = np.compress(view_holder, pieces_a, axis=1).transpose(1, 0)[0]
        factors = np.linalg.solve(viriables, cup)
        key_ori = ''
        for each in factors:
            print("系数拼凑:")
            print(int(each))
            key_ori += str(int(each))
        print("被哈希的:")
        print(key_ori.encode('utf-8'))
        hasher.update(key_ori.encode('utf-8'))
        keys.append(hasher.digest())
        last_curse = i
    print("恢复user keys:")
    print(keys)
    return keys