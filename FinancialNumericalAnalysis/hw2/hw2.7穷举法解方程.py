import math
for m in range(60,81):
    for d in range(60,81):
        for y in range(60,81):
            if 8*m==1*d+6*y and 5*d==4*m+1*y and 7*y==4*m+4*d:
                print ("木工工资:",m,"电工工资:",d,"油漆工工资:",y)
