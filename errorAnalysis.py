import analyticalSolution as exact
from evaluateSpline import evaluateSpline
import matplotlib.pyplot as plt
propFunctDict = {
    'AreaRatio':exact.exactAreaRatio,
    'PressureRatio':exact.exactPressureRatio,
    'TempRatio':exact.exactTempRatio,
    'DensityRatio':exact.exactDensityRatio,
}
def errorAnalysis(machArray,targetSpline,splinesNat,splinesHybrid,splinesParabolic, numOfPoints=10000,TOL=1e-15,eps=1e-15):
    minMach,maxMach = machArray[0], machArray[-1]
    step = (maxMach - minMach)/(numOfPoints-1)
    xArray = []
    yNatArray, yHybridArray, yParaArray,yExactArray = [], [],[],[]
    splineNat = splinesNat[targetSpline]
    splineHybrid = splinesHybrid[targetSpline]
    splineParabolic = splinesParabolic[targetSpline]
    exactPropFunction = propFunctDict[targetSpline]
    errParaArray, errHybridArray, errNatArray = [],[],[]

    


    for i in range(numOfPoints):
        xArray.append(minMach+i*step)
        yNatArray.append(evaluateSpline(xArray[i],splineNat))
        yHybridArray.append(evaluateSpline(xArray[i],splineHybrid))
        yParaArray.append(evaluateSpline(xArray[i],splineParabolic))
        yExactArray.append(exactPropFunction(xArray[i]))
        errNat = abs(yNatArray[i] - yExactArray[i]) +eps
        errPara = abs(yParaArray[i] - yExactArray[i]) +eps
        errHybrid = abs(yHybridArray[i] - yExactArray[i]) +eps
        # if errNat < TOL:
        #     errNat+=eps
        # if errPara < TOL:
        #     errPara+=eps
        # if errHybrid < TOL:
        #     errHybrid+=eps
        errParaArray.append(errPara)
        errHybridArray.append(errHybrid)
        errNatArray.append(errNat)
    
    fig,ax = plt.subplots(3,1,figsize=(16,12))
    ax[0].plot(xArray, errNatArray, 'r-', label='Natural Error')
    ax[1].plot(xArray,errParaArray , 'g-', label='Parabolic Error')
    ax[2].plot(xArray,errHybridArray, color='yellow', linewidth=2.5, label='Hybrid Clamped')
    ax[0].grid()
    ax[0].set_yscale('log')
    ax[1].set_yscale('log')
    ax[2].set_yscale('log')
    plt.tight_layout()
    plt.show()

    
    