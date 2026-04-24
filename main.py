#importing different modules
from dataIngestion import inputData
from buildTrigonalMatrix import buildTridiagonalMatrix
from solveMatrixEquation import solveMatrixEquations
from generateSplineCoefficients import generateSplineCoefficients
from plotGraph import plotCurveWithMach,plotAllSplines, plotCurveWithMachAndTarget, plotCompareSplines
from evaluateSpline import evaluateSpline
from lagrangePoly import generateSlopeDicts
from errorAnalysis import errorAnalysis
from NR import hybrid_newton_bisection

filepath = "Data\isentropic_gas_table.csv"
title = 'Isentropic Flow: Mach Number vs. Area Ratio'
xlabel = 'Mach Number'
ylabel = 'Area Ratio'
targetMach = 1.245
targetSpline = 'AreaRatio'
targetProperty = 7

def main():
    data = inputData(filepath)
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

    # plotCompareSplines(machArray=data['Mach'], splines1=splinesPara[targetSpline], splines2=splinesNat[targetSpline], splines3=splinesHybrid[targetSpline],title=title,xlabel=xlabel,ylabel=ylabel)
    errorAnalysis(data['Mach'],targetSpline,splinesNat,splinesHybrid,splinesPara)

    # print(evaluateSpline(targetMach, splines[targetSpline]))
    # plotAllSplines(
    #     machArray=data['Mach'],
    #     splines= splines,
    #     numOfPoints=1000
    # )
    # plotCurveWithMach(
    #     machArray=data['Mach'], 
    #     splines= splines['AreaRatio'],
    #     title = title,
    #     xlabel=xlabel,
    #     ylabel=ylabel,
    #     numOfPoints=1000,
    #     xMach=True
    #     )
    # plotCurveWithMachAndTarget(
    #     machArray=data['Mach'], 
    #     splines= splines['AreaRatio'],
    #     title = title,
    #     xlabel=xlabel,
    #     ylabel=ylabel,
    #     targetMach=targetMach,
    #     numOfPoints=1000,
    #     xMach=True
    #     )
    


#entry point
main()