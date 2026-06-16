import random
sum=0
for i in range (1000000):
    while 1 :
        x = random.randint(1,100)%3
        if x==0:
            sum+=2
            break
        if x==1:
            sum+=4
        if x==2:
            sum+=6
print(sum/1000000)
