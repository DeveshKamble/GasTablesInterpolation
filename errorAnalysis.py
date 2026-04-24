from contendors import splines, getLinearArray, piecewiseCubicLagrange
import matplotlib.pyplot as plt


def errorAnalysis(machArray,targetSpline,data,splinesNat,splinesHybrid,splinesParabolic, numOfPoints=10000,eps=1e-16):
    minMach,maxMach = machArray[0], machArray[-1]
    step = (maxMach - minMach)/(numOfPoints-1)
    xArray = []
    for i in range(numOfPoints):
        xArray.append(minMach+i*step)
    errLagrangeArray = piecewiseCubicLagrange(xArray,machArray,targetSpline,data,eps)
    errLinearArray = getLinearArray(xArray, machArray,targetSpline,data,eps)
    errNatArray,errParaArray,errHybridArray = splines(xArray, splinesNat, splinesHybrid,splinesParabolic,targetSpline,eps)
    plt.figure()
    plt.plot(xArray,errParaArray , 'g-',linewidth=2.5, label='Parabolic Error')
    plt.plot(xArray, errNatArray, 'r-', linewidth=2,label='Natural Error')
    plt.plot(xArray,errHybridArray, color='yellow',linewidth=1.5, label='Hybrid Clamped Error')
    plt.plot(xArray,errLinearArray, color='blue',linewidth=1, label='Linear Error')
    plt.plot(xArray,errLagrangeArray, color='black',linewidth=0.5, label='Lagrange Error')
    plt.xlabel('Mach Number')
    plt.ylabel('Absolute error')
    plt.yscale('log')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()

    
    