from contendors import splines, getLinearArray, piecewiseCubicLagrange,getExact
import matplotlib.pyplot as plt
import csv
import math

def calcMaxError(errArray): 
    return max(errArray)
def calcMae(errArray): 
    total = 0
    for e in errArray:
        total+= e
    return total / len(errArray)
def calcRmse(errArray): 
    total = 0
    for e in errArray:
        total+= e**2 
    return math.sqrt( total/ len(errArray))
def calcMape(errArray, exactArray):
    eps = 1e-16
    total =0 
    for i in range(len(errArray)):
        total += errArray[i]/(abs(exactArray[i])+eps)
    return (total / len(errArray)) * 100.0

def exportStatisticsToCsv(filename, errLagrangeArray, errLinearArray, errNatArray, errParaArray, errHybridArray, exactArray=None):
    models = {
        'Local Lagrange': errLagrangeArray,
        'Linear Interpolation': errLinearArray, 
        'Natural Spline': errNatArray,
        'Parabolic Spline': errParaArray,
        'Hybrid Clamped Spline': errHybridArray
    }
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        if exactArray is not None:
            writer.writerow(['Model Name', 'Max Error (Worst Case)', 'RMSE (Overall Fit)', 'MAE (Average Error)', 'MAPE (%)'])
        else:
            writer.writerow(['Model Name', 'Max Error (Worst Case)', 'RMSE (Overall Fit)', 'MAE (Average Error)'])
        for modelName, errArray in models.items():
            maxErr = calcMaxError(errArray)
            rmse = calcRmse(errArray)
            mae = calcMae(errArray)
            rowData = [
                modelName, 
                f"{maxErr}", 
                f"{rmse}", 
                f"{mae}"
            ]     
            if exactArray is not None:
                mape = calcMape(errArray, exactArray)
                rowData.append(f"{mape}")  
            writer.writerow(rowData)      
    print(f"statistical report generated: '{filename}'")

    
    
def errorAnalysis(machArray,targetSpline,data,splinesNat,splinesHybrid,splinesParabolic, numOfPoints=10000,eps=1e-16):
    #Making the test mach array
    minMach,maxMach = machArray[0], machArray[-1]
    step = (maxMach - minMach)/(numOfPoints-1)
    xArray = []
    for i in range(numOfPoints):
        xArray.append(minMach+i*step)

    #Finding the error for each of the method
    errLagrangeArray = piecewiseCubicLagrange(xArray,machArray,targetSpline,data,eps)
    errLinearArray = getLinearArray(xArray, machArray,targetSpline,data,eps)
    errNatArray,errParaArray,errHybridArray = splines(xArray, splinesNat, splinesHybrid,splinesParabolic,targetSpline,eps)
    
    #plotting all the errors
    plt.figure()
    plt.plot(xArray,errParaArray , 'red',linewidth=2.5, label='Parabolic Error')
    plt.plot(xArray, errNatArray, 'yellow', linewidth=2,label='Natural Error')
    plt.plot(xArray,errHybridArray, color='green',linewidth=1.5, label='Hybrid Clamped Error')
    plt.plot(xArray,errLinearArray, color='blue',linewidth=1.25, label='Linear Error')
    plt.plot(xArray,errLagrangeArray, color='black',linewidth=1, label='Lagrange Error')
    plt.xlabel('Mach Number')
    plt.ylabel('Absolute error')
    plt.yscale('log')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()

    #Calculating the Statistics
    exactArray = getExact(targetSpline,xArray)
    exportStatisticsToCsv('statistics', errLagrangeArray,errLinearArray, errNatArray,errParaArray,errHybridArray,exactArray)



