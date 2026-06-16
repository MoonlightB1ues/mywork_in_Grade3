sum1=0
for i in range(1,51):
    sum1+=i**3/i/(i+2)
print("for循环得到的结果为:",sum1)
sum2=0
i=1
while i<51:
    sum2+=i**3/i/(i+2)
    i+=1
print("while循环得到的结果为:",sum2)
