#importing different modules
from dataIngestion import inputData
from buildTrigonalMatrix import buildTrigonalMatrix
from solveMatrixEquation import solveMatrixEquations
from generateSplineCoefficients import generateSplineCoefficients
from plotGraph import plotCurveWithMach,plotAllSplines
from evaluateSpline import evaluateSpline

filepath = "Data\isentropicTables.csv"
title = 'Isentropic Flow: Mach Number vs. Area Ratio'
xlabel = 'Mach Number'
ylabel = 'Area Ratio'
targetMach = 3.55
targetSpline = 'AreaRatio'

def main():
    data = inputData(filepath)
    lower,main,upper,rhs = buildTrigonalMatrix(data)
    sol = solveMatrixEquations(lower,main,upper,rhs)
    splines = generateSplineCoefficients(sol, data)
    print(evaluateSpline(targetMach, splines[targetSpline]))
    plotAllSplines(
        machArray=data['Mach'],
        splines= splines,
        numOfPoints=1000
    )
    plotCurveWithMach(
        machArray=data['Mach'], 
        splines= splines['AreaRatio'],
        title = title,
        xlabel=xlabel,
        ylabel=ylabel,
        numOfPoints=1000,
        xMach=True
        )


#entry point
main()