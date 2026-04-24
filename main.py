#importing different modules
from dataIngestion import inputData
from buildTrigonalMatrix import buildTridiagonalMatrix
from solveMatrixEquation import solveMatrixEquations
from generateSplineCoefficients import generateSplineCoefficients
from plotGraph import plotCurveWithMach,plotAllSplines, plotCurveWithMachAndTarget, plotCompareSplines
from evaluateSpline import evaluateSpline
from lagrangePoly import generateSlopeDicts
from errorAnalysis import errorAnalysis
from NR import hybridNewtonBisection
import analyticalSolution as exact

targetMach = 1.245
targetSpline = 'AreaRatio'
targetProperty = 7

def main():
    minMach, maxMach, numPoints = 0.1, 3.0, 30
    step = (maxMach - minMach) / (numPoints - 1)
    machArray = [minMach + i * step for i in range(numPoints)]
    
    data = {
        'Mach': machArray,
        'PressureRatio': [exact.exactPressureRatio(m) for m in machArray],
        'DensityRatio': [exact.exactDensityRatio(m) for m in machArray],
        'TemperatureRatio': [exact.exactTempRatio(m) for m in machArray],
        'AreaRatio': [exact.exactAreaRatio(m) for m in machArray]
    }
    slopeStart,slopeEnd = generateSlopeDicts(data)
    lower,main,upper,rhs = buildTridiagonalMatrix(data,mode='parabolic')
    sol = solveMatrixEquations(lower,main,upper,rhs)
    splinesPara = generateSplineCoefficients(sol, data)

    lower,main,upper,rhs = buildTridiagonalMatrix(data,mode='natural')
    sol = solveMatrixEquations(lower,main,upper,rhs)
    splinesNat = generateSplineCoefficients(sol, data)
   
    lower,main,upper,rhs = buildTridiagonalMatrix(data,mode='clamped', slopeStart=slopeStart, slopeEnd=slopeEnd)
    sol = solveMatrixEquations(lower,main,upper,rhs)
    splinesHybrid = generateSplineCoefficients(sol, data)

    


#entry point
main()