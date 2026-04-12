def findCoeff(machArray, dataArray, sol):
    n = len(machArray)
    spline = []
    for i in range(n-1):
        h = machArray[i+1] - machArray[i]
        a = dataArray[i]
        b = ((dataArray[i+1]-dataArray[i])/h - (h * (2*sol[i] + sol[i+1]))/6)
        c = sol[i]/2
        d = (sol[i+1] - sol[i])/(6*h)
        spline.append({
            'Mach_start':machArray[i],
            'Mach_end':machArray[i+1],
            'a':a,
            'b':b,
            'c':c,
            'd':d,
        })
    return spline

def generateSplineCoefficients(sol,data):
    machArray = data['Mach']
    splines = {}
    for header, value in sol.items():
        spline = findCoeff(machArray, data[header], value)
        splines[header] = spline
    # print(splines)
    return splines