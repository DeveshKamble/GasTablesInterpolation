#importing different modules
from dataIngestion import inputData
from buildTrigonalMatrix import buildTrigonalMatrix
from solveMatrixEquation import solveMatrixEquations
from generateSplineCoefficients import generateSplineCoefficients
from plotGraph import plotCurveWithMach,plotAllSplines, plotCurveWithMachAndTarget
from evaluateSpline import evaluateSpline
from NR import hybrid_newton_bisection

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
    target_area = 100

    # 1. Subsonic Search: Cage the root strictly between M=0.001 and M=0.999
    subsonic_mach = hybrid_newton_bisection(
        target_area, 
        bound_a=0.001, 
        bound_b=0.999, 
        splines=splines['AreaRatio']
    )

    # 2. Supersonic Search: Cage the root strictly between M=1.001 and your maximum table value
    supersonic_mach = hybrid_newton_bisection(
        target_area, 
        bound_a=1.001, 
        bound_b=30.0, 
        splines=splines['AreaRatio']
    )

    # Remember to apply rounding ONLY at the very end
    print(f"Target Area Ratio: {target_area}")
    if subsonic_mach: print(f"Subsonic M:   {subsonic_mach:.4f}")
    if supersonic_mach: print(f"Supersonic M: {supersonic_mach:.4f}")
    print(evaluateSpline(targetMach, splines[targetSpline]))
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
    plotCurveWithMachAndTarget(
        machArray=data['Mach'], 
        splines= splines['AreaRatio'],
        title = title,
        xlabel=xlabel,
        ylabel=ylabel,
        targetMach=targetMach,
        numOfPoints=1000,
        xMach=True
        )
    #add function to plot curve of mach and target spline, along with the tagret ratio shown as line on the graph
    


#entry point
main()