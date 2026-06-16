sum=0
for k in range(1,1000000+2):
    sum+=k*(1+1/1000000)**(1000000+1-k)
print(sum)