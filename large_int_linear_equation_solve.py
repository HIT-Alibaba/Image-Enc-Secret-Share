# # -*- coding: utf-8 -*-
#
# __author__ = 'alex'
#
# '''
# Created on 2013年10月12日
#
# @author: yanghl
# 迭代法解线性方程组,迭代法有局限，某些问题处理不了
# '''
# import numpy as np
# import scipy.linalg as linalg  # scipy中求解线性方程组的库
#
#
# def dot(matrix1, matrix2):
#     '''给定两个矩阵1和2，其中矩阵1是a×n的，矩阵2是n×b的
#     返回它们矩阵乘积:a×b矩阵
#     '''
#     tmp = 0
#     if len(matrix1.shape) == 1:
#         m1 = [matrix1.tolist()]
#     else:
#         m1 = matrix1.tolist()
#     if len(m1) == 0 or len(m1[0]) == 0:
#         return np.array([0])
#     if len(matrix2.shape) == 1:
#         m2 = [matrix2.tolist()]
#     else:
#         m2 = matrix2.tolist()
#     if len(m2) == 0 or len(m2[0]) == 0:
#         return np.array([0])
#     a = len(m1)
#     n = len(m1[0])
#     b = len(m2[0])
#     result = [[0] * b for row in range(a)]
#     for i in range(0, a):
#         for j in range(0, b):
#             for k in range(0, n):
#                 result[i][j] += m1[i][k] * m2[k][j]
#     return np.array(result)
#
#
# def transpose(matrix):
#     x = len(matrix)
#     y = len(matrix[0])
#     result = [[0] * y for row in range(x)]
#     for i in range(0, x):
#         for j in range(0, y):
#             result[j][i] = matrix[i][j]
#     return result
#
#
# def iterate(A, B, X0, e, k_max):
#     """
#     迭代法求解线性方程组，AX=B,X0为初始值，系数矩阵为非奇异矩阵,delta为精度
#     k_max 为最大循环次数，e为要求精度
#     """
#     B = B.T
#     X_k = X0
#     X_k1 = np.zeros(X0.shape)
#     n = B.shape[0]
#     delta = 10
#     k = 0 #循环次数
#     while delta > e:
#         for i in range(n):
# #             print i,B[i],A[i,0:i],X_k1[0:i],A[i,i:n],X_k[i:n],A[i,i]
#             X_k1[i] = 1.0*(B[i]-np.dot(A[i,0:i],X_k1[0:i])[0]-np.dot(A[i,i+1:n],X_k[i+1:n])[0])/A[i,i]
#         #         print i,X_k1[i]
#         delta = max(abs(X_k1-X_k))
#         X_k = X_k1.copy()
#         result = X_k.T[0]
#         k += 1
#         if k > k_max:
#             return result, delta
#     return result, delta
#
#
# if __name__ == "__main__":
#     A = np.array([[1, 1], [1, -1]])
#     # B = np.array([[5, 1]])
#     B = np.array([5, 1])
#     Bp = np.array([5, 1])
#
#     # B = np.array([[1922732992239235470]])
#     X0 = np.array([[0], [0]])
#     e = 1
#     k_max = 100
#     x1 = iterate(A, B, X0, e, k_max)[0]
#     print(x1)
#
#     x = linalg.solve(A, Bp)
#     print(x)  # 调用scipy中求解线性方程组的包，验证结果

import numpy as np
import scipy.linalg as linalg #scipy中求解线性方程组的库

def iterate(A,B,X0,e,k_max):
    """
    迭代法求解线性方程组，AX=B,X0为初始值，系数矩阵为非奇异矩阵,delta为精度
    k_max 为最大循环次数，e为要求精度
    """
    B = B.T
    X_k = X0
    X_k1 = np.zeros(X0.shape, dtype=B.dtype)
    n = B.shape[0]
    delta = 10
    k = 0 #循环次数
    while delta > e:
        for i in range(n):
#             print i,B[i],A[i,0:i],X_k1[0:i],A[i,i:n],X_k[i:n],A[i,i]
            X_k1[i] = 1.0*(B[i]-np.dot(A[i,0:i],X_k1[0:i])[0]-np.dot(A[i,i+1:n],X_k[i+1:n])[0])//A[i,i]
        #         print i,X_k1[i]
        delta = max(abs(X_k1-X_k))
        X_k = X_k1.copy()
        result = X_k.T[0]
        k = k + 1
        if k > k_max:
            return result,delta
    return result,delta


if __name__ == "__main__":
#     A = np.array([[2,-1,0],
#               [1,-2,1],
#               [0,-1,2]])
#     B = np.array([500,0,100])

    A = np.array([[11,-5,0,0,0,-1],
                  [4,-13,3,0,6,0],
                  [0,3,-7,5,0,0],
                  [0,0,1,-4,3,0],
                  [0,1,0,2,-4,1],
                  [2,0,0,0,15,-47]
                  ])
    B = np.array([500,0,0,0,0,0])
    X0 = np.array([[0],[0],[0],[0],[0],[0]])
    e = 1e-10
    k_max = 100
    x1 = iterate(A, B, X0, e,k_max)[0]
    print(x1)

    x = linalg.solve(A,B)
    print(x)   #调用scipy中求解线性方程组的包，验证结果