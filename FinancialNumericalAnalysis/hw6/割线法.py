def secant(x0,x1,e):
    f0=equation(x0)
    f1=equation(x1)
    x2=x1-f1/((f1-f0)/(x1-x0))
    while abs(x2-x1)>e:
        x0=x1
        f0=f1
        x1=x2
        f1=equation(x1)
        x2=x2-f1/((f1-f0)/(x1-x0))
    root=x2
    return root

def equation(x):
    f=x**3+2*x**2+10*x-20
    return f

print(secant(0,1,1e-6))
