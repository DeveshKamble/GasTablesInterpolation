def solveTridiagonalSystem(lower,main,upper,rhs):
    n = len(main)
    x = [0]*n
    c_prime,d_prime = [0]*n,[0]*n
    c_prime[0] = upper[0]/main[0]
    d_prime[0] = rhs[0]/main[0]

    #Forward sweep 
    for i in range(1,n):
        m = main[i] - lower[i]*c_prime[i-1]
        c_prime[i] = upper[i]/m
        d_prime[i] = (rhs[i] - lower[i]*d_prime[i-1])/m

    #Backward substitution
    x[n-1] = d_prime[n-1]
    
    for i in range(n-2,-1,-1):
        x[i] = d_prime[i] - c_prime[i]*x[i+1]
    print("Solution found")
    # print(x)
    return x
    

def solveMatrixEquations(lower,main,upper,rhs):
    #we have to solve Ax = rhs for each of the dependent quantity
    # A is made from lower, main and upper
    sol = {}
    headers = list(rhs.keys())
    print(headers)
    for header in headers:
        sol[header] = []

    for header,b in rhs.items():
        print(f"Solving {header} equation")
        sol[header] = solveTridiagonalSystem(lower,main,upper,b)
        
    
    # print(sol)
    return sol