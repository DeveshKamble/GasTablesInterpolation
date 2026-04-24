def localCubicLagrange(xTarget, xArray, yArray):
    n = len(xArray)
    index = 0
    for i in range(n-1):
        if xArray[i] <= xTarget <= xArray[i+1]:
            index = i
            break
    else:
        index = n - 2 
    if index == 0: 
        indices = [0, 1, 2, 3]
    elif index == n - 2: 
        indices = [n-4, n-3, n-2, n-1]
    else: 
        indices = [index-1, index, index+1, index+2]
    yValue = 0.0
    for j in indices:
        term = yArray[j]
        for m in indices:
            if m != j:
                term *= (xTarget - xArray[m]) / (xArray[j] - xArray[m])
        yValue += term
    return yValue

def estimateLagrangeSlope(xArray, yArray, targetIndex):
    n = len(xArray)
    xTarget = xArray[targetIndex]
    slope = 0.0
    
    for i in range(n):
        #denominator is constant for Li(x)
        denominator = 1
        for j in range(n):
            if i != j:
                denominator *= (xArray[i] - xArray[j])
        numerator = 0
        for j in range(n):
            if i != j:
                term = 1.0
                for k in range(n):
                    if k != i and k != j:#removed because by chain rule jth term is differentiated to 1
                        term *= (xTarget - xArray[k])
                numerator += term
        
        slope += yArray[i] * (numerator / denominator)
        
    return slope

def generateSlopeDicts(data, pointsToUse=4):
    machArray = data['Mach']
    headers = list(data.keys())
    headers.remove('Mach')
    
    slopeStart = {}
    slopeEnd = {}
    
    for header in headers:
        values = data[header]
        
        slopeStart[header] = estimateLagrangeSlope(
            machArray[:pointsToUse], #using the first n points of the array
            values[:pointsToUse], 
            targetIndex=0
        )

        slopeEnd[header] = estimateLagrangeSlope(
            machArray[-pointsToUse:], #using the last n points of the array
            values[-pointsToUse:], 
            targetIndex=pointsToUse - 1
        )
        
    return slopeStart, slopeEnd
