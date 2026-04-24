
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
def buildTridiagonalMatrix(data,mode = 'parabolic', slopeStart=None, slopeEnd=None):
    #Mach number is the independent quantity
    h = calculateStep(data)
    n = len(data['Mach'])
    #forming the traigonal matrix
    lower = [0.0]*n # forms array of length n that have all entries as 0
    main = [0.0]*n
    upper = [0.0]*n

    if mode == 'parabolic':
        #we do not know the slopes at the start and the end thus we cannot use clamped cubic splines
        #however using natural cubic spline may give arbitrary results 
        #we are using parabolic approximation at the boundaries

        # M0 = M1 giving parabolic approximation as d = (M1-M0)/6h[0]
        main[0] = 1
        upper[0] = -1

        # M(n-2) = M(n-1)
        main[n-1] = 1
        lower[n-1] = -1
    elif mode == 'natural':
        main[0] = 1
        upper[0] = 0
        main[n-1] = 1
        lower[n-1] = 0
    elif mode == 'clamped':
        main[0] = 2*h[0]
        upper[0] = h[0]
        main[n-1] = 2*h[n-2]
        lower[n-1] = h[n-2]
    else:
        print("Please select one of the following modes for building Tridiagonal System:natural, clamped or parabolic")
        return

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
    for header, values in dataIndependant.items(): #This has constant items(5) so overall this function implements in O(n) time complexity
        tempRhs = [0]*n

        for i in range(1,n-1): #the calue of tempPhs at i=0 and n-1 must be 0 because of parabolic approximation at the ends
            tempRhs[i] = 6.0*( (values[i+1]-values[i])/h[i] - (values[i] - values[i-1])/h[i-1] )
        if mode == "clamped":
            # For clamped, we use the slopes (either analytical or Lagrange-estimated)
            tempRhs[0] = -6.0 * (values[0] - values[1]) / h[0] - 6.0 * slopeStart[header]
            tempRhs[n-1] = 6.0 * (values[n-2] - values[n-1]) / h[n-2] + 6.0 * slopeEnd[header]
         
        rhs[header] = tempRhs

    return lower, main, upper, rhs


