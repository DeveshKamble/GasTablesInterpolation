import matplotlib.pyplot as plt
from evaluateSpline import evaluateSpline

def plotCurveWithMach(machArray,splines, title, xlabel, ylabel, numOfPoints = 500, xMach=True):
    minMach = machArray[0]
    maxMach = machArray[-1]
    step = (maxMach - minMach)/(numOfPoints-1)
    xArray = []
    yArray = []
    for i in range(numOfPoints):
        xArray.append(minMach + i*step)
        yArray.append(evaluateSpline(xArray[i], splines))
    # print(len(xArray), len(yArray))
    plt.figure()
    if xMach:
        plt.plot(xArray, yArray, color='blue', linewidth=2)
    if not xMach:
        plt.plot(yArray, xArray, color='blue', linewidth=2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()

def plotCompareSplines(machArray,splines1,splines2,splines3, title, xlabel, ylabel, numOfPoints = 500):
    minMach = machArray[0]
    maxMach = machArray[-1]
    step = (maxMach - minMach)/(numOfPoints-1)
    xArray1 = []
    yArray1 = []
    for i in range(numOfPoints):
        xArray1.append(minMach + i*step)
        yArray1.append(evaluateSpline(xArray1[i], splines1))
    # print(len(xArray1), len(yArray1))
    


    xArray2 = []
    yArray2 = []
    for i in range(numOfPoints):
        xArray2.append(minMach + i*step)
        yArray2.append(evaluateSpline(xArray2[i], splines2))
    # print(len(xArray2), len(yArray2))

    
 
    xArray3 = []
    yArray3 = []
    for i in range(numOfPoints):
        xArray3.append(minMach + i*step)
        yArray3.append(evaluateSpline(xArray3[i], splines3))
    # print(len(xArray3), len(yArray3))
    plt.figure()
    plt.plot(xArray1, yArray1, color='blue',label='spline Parabolic', linewidth=2)
    plt.plot(xArray2, yArray2, color='yellow',label='spline Natural', linewidth=2)
    plt.plot(xArray3, yArray3, color='red',label='spline Hybrid', linewidth=2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()

def plotCurveWithMachAndTarget(machArray,splines, title, xlabel, ylabel,targetMach, numOfPoints = 500, xMach=True):
    minMach = machArray[0]
    maxMach = machArray[-1]
    step = (maxMach - minMach)/(numOfPoints-1)
    xArray = []
    yArray = []
    
    for i in range(numOfPoints):
        xArray.append(minMach + i*step)
        yArray.append(evaluateSpline(xArray[i], splines))
        
    # print(len(xArray), len(yArray))
    plt.figure()
    if xMach:
        plt.plot(xArray, yArray, color='blue', linewidth=2)
    if not xMach:
        plt.plot(yArray, xArray, color='blue', linewidth=2)
    maxY = max(yArray)
    targetY = [ i for i in range(len(yArray))]
    targetX = [targetMach]*len(targetY)
    plt.plot(targetX, targetY, color='red', linewidth=2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()


def plotAllSplines(machArray,splines, numOfPoints = 500):
    pressureSpline = splines['PressureRatio']
    densitySpline = splines['DensityRatio']
    temperatureSpline = splines['TemperatureRatio']
    areaSpline = splines['AreaRatio']
    step = (machArray[-1] - machArray[0])/(numOfPoints-1)
    xArray = []
    pressureArray = []
    densityArray = []
    temperatureArray = []
    areaArray = []
    machInitial = machArray[0]
    for i in range(numOfPoints):
        xArray.append(machInitial + i*step)
        pressureArray.append(evaluateSpline(xArray[i],pressureSpline))
        densityArray.append(evaluateSpline(xArray[i],densitySpline))
        temperatureArray.append(evaluateSpline(xArray[i],temperatureSpline))
        areaArray.append(evaluateSpline(xArray[i],areaSpline))
    
    plt.figure()
    plt.plot(xArray, pressureArray, color = 'red', linewidth = 2, label = 'Pressure Ratio')
    plt.plot(xArray, densityArray, color = 'blue', linewidth = 2, label='Density Ratio')
    plt.plot(xArray, temperatureArray, color = 'black', linewidth = 2, label = 'Temperature Ratio')
    plt.plot(xArray, areaArray, color = 'yellow', linewidth = 2, label = 'Area Ratio')
    plt.legend()
    plt.xlabel('Mach Number')
    plt.grid()
    plt.show()
