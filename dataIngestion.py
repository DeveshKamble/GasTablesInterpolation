import csv

#Take file path as the input parameter in string format 
#Returns a dictionary with array of data corresponding to each header in following format as output
#data = {
# 'Mach': [.....]
# 'PressureRatio':[......]
#  ......
#}
def inputData(path):
    data = {}   

    with open(path, mode= "r") as file:
        f = csv.reader(file)
        #skip the headers in csv file
        #M, Po/P, rho0/rho, To/T, A/A*
        next(f)
        #USing custom headers for easier understanding
        headers = ['Mach', 'PressureRatio', 'DensityRatio', 'TemperatureRatio', 'AreaRatio']
        
        #print(headers)
        for header in headers:
            data[header] = []  #for each of the header make an array to store all the data
        
        #appending the data values to each header
        for row in f:
            # print(row)
            for i in range(len(row)):
                data[headers[i]].append(float(row[i])) #This adds the data value of that row to the respective header
        return data


#Testing
#print(inputMatrix('Data\inputData.csv'))


