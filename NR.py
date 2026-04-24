from evaluateSpline import evaluateSpline, evaluateSplineDerivative
def hybridNewtonBisection(targetY, boundA, boundB, splines, tol=1e-6, maxIter=100):
    
    #solving f(x) = S(x) - targetY = 0
    y_a = evaluateSpline(boundA, splines)
    y_b = evaluateSpline(boundB, splines)
    
    f_a = y_a- targetY
    f_b = y_b- targetY
    
    #root is in the interval if the signs are opposite
    if f_a * f_b > 0:
        print(f"The root is not bracketed between Mach {boundA} and {boundB}")
        return None
        
    x_n = (boundA + boundB)/2
    
    for i in range(maxIter):
        currentY = evaluateSpline(x_n,splines)
        slope = evaluateSplineDerivative(x_n,splines)
        f_x = currentY - targetY
        
        if abs(f_x) < tol:
            return x_n
        if slope != 0.0:
            newtonStep = f_x/slope
            xNextNewton = x_n-newtonStep
        else:
            xNextNewton = boundA - 1.0
        # Check if the step is strictly inside the bounds
        if (boundA< xNextNewton <boundB):
            xNext = xNextNewton
        else:
            # out of bounds, making new guess
            xNext = (boundA+boundB) /2

        yNext= evaluateSpline(xNext, splines)
        f_next = yNext - targetY
        
        # cheching sings of function values
        if f_a * f_next > 0:
            boundA = xNext
            f_a = f_next
        else:
            boundB = xNext
            f_b = f_next
            
        #guess for the next iteration
        x_n = xNext
        
    print(f"Hybrid Solver Failed to converge after {maxIter} iterations.")
    return x_n

