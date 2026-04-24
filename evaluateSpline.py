def evaluateSpline(x, splines):
    for spline in splines:
        if spline['Mach_start'] <= x <= spline['Mach_end']:
            dx = x - spline['Mach_start']
            result = spline['a'] + spline['b']*dx + spline['c']*pow(dx,2) + spline['d']*pow(dx,3)
            return result


def evaluateSplineDerivative(x, splines):
    if x < splines[0]['Mach_start']:
        #the target x is less than that of the first data point
        # extrapolating the first spline
        spline = splines[0]
        dx = x - spline['Mach_start']
        return spline['a'] + spline['b']*dx + spline['c']*pow(dx,2) + spline['d']*pow(dx,3)
    for spline in splines:
        if spline['Mach_start'] <= x <= spline['Mach_end']:
            dx = x - spline['Mach_start']
            result = spline['a'] + spline['b']*dx + spline['c']*pow(dx,2) + spline['d']*pow(dx,3)
            return result
    #the x value is greater than the last Mach number data point
    # extrapolating the final spline
    spline = splines[-1]
    dx = x - spline['Mach_start']
    return spline['b'] + 2*spline['c']*pow(dx,1) + 3*spline['d']*pow(dx,2)
      
