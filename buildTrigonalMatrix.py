def calculateStep(data):
    h = []
    machArray = data['Mach']
    # print(machArray)
    prev = machArray[0]
    for m in machArray[1:]: # starting the iteration from second element of array
        h.append(m - prev)
        prev = m
    
    return h

#takes input as the data dictionary 
#output is the lower, main and upper diagonal of the triagonal matrix 
#along with the right hand side of all the independent parameters
def buildTrigonalMatrix(data):
    #Mach number is the independent quantity
    h = calculateStep(data)
    n = len(data['Mach'])
    #forming the traigonal matrix
    lower = [0.0]*n # forms array of length n that have all entries as 0
    main = [0.0]*n
    upper = [0.0]*n

    #we do not know the slopes at the start and the end thus we cannot use clamped cubic splines
    #however using natural cubic spline may give arbitrary results 
    #we are using parabolic approximation at the boundaries

    # M0 = M1 giving parabolic approximation as d = (M1-M0)/6h[0]
    main[0] = 1.0
    upper[0] = -1.0

    # M(n-2) = M(n-1)
    main[n-1] = 1.0
    lower[n-1] = -1.0

    #calculating all the three diagonals as if clamped cubic spline
    for i in range(1,n-1):
        lower[i] = h[i-1]
        main[i] = 2*(h[i] + h[i-1])
        upper[i] = h[i]

    #dict to store the rhs for all the dependent quantities to generate the cubic splines
    rhs = {}
    headers = list(data.keys())
    headers.remove('Mach')
    #print(headers)
    for header in headers:
        rhs[header] = []
    
    dataIndependant = data.copy()
    dataIndependant.pop('Mach')
    # print(dataIndependant.keys())
    #generating the rhs for each of the dependant parameters
    for header, values in dataIndependant.items():
        tempRhs = [0]*n

        for i in range(1,n-1): #the calue of tempPhs at i=0 and n-1 must be 0 because of parabolic approximation at the ends
            tempRhs[i] = 6.0*( (values[i+1]-values[i])/h[i] - (values[i] - values[i-1])/h[i-1] )
        
        rhs[header] = tempRhs

    return lower, main, upper, rhs



