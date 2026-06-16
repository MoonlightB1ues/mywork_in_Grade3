import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

def LU(A):
    n=len(A[:,0])
    L=np.eye(n)
    U=np.zeros((n,n))
    U[0,:]=A[0,:]
    L[0:n,0]=A[0:n,0]/U[0,0]
    for i in range(1,n):
        U[i,i:n]=A[i,i:n]-np.dot(L[i,0:i],U[0:i,i:n])
        L[i+1:n,i]=(A[i+1:n,i]-np.dot(L[i+1:n,0:i],U[0:i,i]))/U[i,i]
    #LU分解
    return L,U



def BI(U,g,n):     # 求解出每个x的值,并以列表存储,用于上三角矩阵求根
    x=np.zeros([n,1])
    x[n-1]=g[n-1]/U[n-1,n-1]
    for i in range(n-2,-1,-1):
        x[i]=(g[i]-np.dot(U[i,i+1:],x[i+1:]))/U[i,i]
    root=x
    return root

def BI1(U,g,n):     # 求解出每个x的值,并以列表存储,用于下三角矩阵求根
    x=np.zeros([n,1])
    x[0]=g[0]/U[0,0]
    for i in range(0,n,1):
        x[i]=(g[i]-np.dot(U[i,0:i],x[0:i]))/U[i,i]
    root=x
    return root

A=np.array([2.0,1,-1,2,4,4,1,3,-6,-1,10,10,-2,1,8,4]).reshape(4,4)
b=np.array([2.0,4,-5,1]).reshape(4,1)

L,U=LU(A)
B=BI1(L,b,4)
print(B)
C=BI(U,B,4)
print(C)
