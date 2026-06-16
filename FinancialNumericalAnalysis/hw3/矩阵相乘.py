import numpy as np
a=np.array([3,1,1,2,1,2,1,2,3]).reshape(3,3)
#print(a)
b=np.array([1,1,-1,2,-1,0,1,-1,1]).reshape(3,3)
#print(b)
q1=2*a+b
#print("2A+B=",q1)
q2=4*a**2-3*b**2
#print("4A^2-3B^2=",q2)
q3=a@b
#print("a*b=",q3)
q4=b@a
print("b*a=",q4)
print(np.dot(b,a))
q5=q3-q4
#print("q5=",q5)
