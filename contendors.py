import analyticalSolution as exact
from evaluateSpline import evaluateSpline
from lagrangePoly import localCubicLagrange

### Note: eps(epsilon) is added to each of the err array element to make sure that if the error approaches 0 then its log plot is not an issue
propFunctDict = {
    'AreaRatio':exact.exactAreaRatio,
    'PressureRatio':exact.exactPressureRatio,
    'TempRatio':exact.exactTempRatio,
    'DensityRatio':exact.exactDensityRatio,
}

def getExact(targetSpline,xArray):
    exactPropFunction = propFunctDict[targetSpline]
    yExactArray = []
    for i in range(len(xArray)):
        yExactArray.append(exactPropFunction(xArray[i]))
    return yExactArray


def piecewiseCubicLagrange(xArray, machArray,targetSpline, data,eps):
    propArray = data[targetSpline]
    yExactArray = getExact(targetSpline,xArray)
    errLagrangeArray = []
    for i in range(len(xArray)):
        yValue = localCubicLagrange(xArray[i], machArray, propArray)
        errLagrangeArray.append(abs(yValue - yExactArray[i])+eps)
    return errLagrangeArray



def linearInter(xtarget, machArray,targetSpline):
    for i in range(len(machArray)-1):
        if machArray[i] <= xtarget <= machArray[i+1]:
            dx = xtarget - machArray[i]
            slope = (targetSpline[i+1] -targetSpline[i])/(machArray[i+1] -machArray[i])
            return targetSpline[i] +slope*dx

def getLinearArray(xArray,machArray,targetSpline,data,eps):
    yExactArray = getExact(targetSpline, xArray)
    yLinearArray = []
    errLinearArray = []
    for i in range(len(xArray)):
        yLinearArray.append(linearInter(xArray[i],machArray,data[targetSpline]))
        errLinearArray.append(abs(yLinearArray[i] - yExactArray[i])+eps)
    return errLinearArray
    

def splines(xArray, splinesNat,splinesHybrid, splinesParabolic, targetSpline,eps = 1e-15):
   
    yNatArray, yHybridArray, yParaArray = [], [],[]
    yExactArray = getExact(targetSpline, xArray)
    splineNat = splinesNat[targetSpline]
    splineHybrid = splinesHybrid[targetSpline]
    splineParabolic = splinesParabolic[targetSpline]
    errParaArray, errHybridArray, errNatArray = [],[],[]
    for i in range(len(xArray)):
        yNatArray.append(evaluateSpline(xArray[i],splineNat))
        yHybridArray.append(evaluateSpline(xArray[i],splineHybrid))
        yParaArray.append(evaluateSpline(xArray[i],splineParabolic))
        errParaArray.append(abs(yParaArray[i] - yExactArray[i]) +eps)
        errHybridArray.append(abs(yHybridArray[i] - yExactArray[i]) +eps)
        errNatArray.append(abs(yNatArray[i] - yExactArray[i]) +eps)
    
    return errNatArray,errParaArray,errHybridArray