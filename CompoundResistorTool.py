# Tool for calculating compound resistor values using E12 preferred series
# Disclaimer: I am not a programmer and this code is probably really shit to run, so don't judge me
# By Kurt Querengesser
# Version 1.0
# 2021-10-01

#TODO: Blacklist, whitelist, pot tolerance, potentiometer standard values

#E12 preferred series values
e12series = [1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2] 
#List of valid resistor suffixes
suffixSeries = ["k", "m"]
#Values associated with said suffixes
multiplierSeries = [1000, 1000000]
#Values considered valid for input string
validVals = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
for i in suffixSeries:
    validVals.append(i)

INVALID = -1
DEFAULT_TOL = 5

resistorTol = 5

########################  Function definitions  #######################

# checks if input is valid
def isValid(strIn):
    count = 0
    for v in validVals: 
        for i in strIn:
            if (i == v):
                count+=1
    if (count != len(strIn)):
        print("Error: invalid chars")
        return(False)
    else:
        return(True)

# ascertains suffix from string and returns multiplier value based on it
# also returns -1 if input is invalid
def getMultiplier(strIn):
    strIn = strIn.lower()

    suffixes = []
    for pos, char in enumerate(strIn):
        for i in suffixSeries:
            if (char == i):
                suffixes.append(i)

    if (len(suffixes) == 0): # no suffix, 1x multiplier
        #print("1x multiplier")
        return(1)
    elif (len(suffixes) > 1): # more than one suffix, invalid
        print("Invalid number of suffixes")
        return(INVALID)
    elif (len(suffixes)  == 1): # 1 suffix, returns multiplier if valid
        temp = multiplierSeries[suffixSeries.index(suffixes[0])]
        #print(str(temp) + "x Multiplier")
        return(int(temp))
    else:
        print("Error: undefined error")
        return(INVALID)


# This function replaces the suffix with a "." if necessary
# it then returns the string as an float.
def replaceSuffix(strIn): 
    strIn = strIn.lower()
    valid = False
    # first thing to do is check if it contains a suffix
    # if it does not, we can ignore it
    for i in suffixSeries:
        if (strIn.find(i) != INVALID):
            valid = True
    if (not valid): # skip
        return(float(strIn)) 
    
    # at this point we must replace the suffix
    for i in suffixSeries:
        strIn = strIn.replace(i, ".")
    return(float(strIn))

def calcResistor(resistorMin):
    change = 1
    while not(resistorMin < e12series[-1] and resistorMin > e12series[0]):
        if (resistorMin < e12series[0] or (resistorMin > e12series[-1] and resistorMin < 10)):
            break
        resistorMin /= 10
        change *= 10
    
    for i in range(len(e12series)-1, -1, -1):
        if (e12series[i] <= resistorMin):
            break
    return(e12series[i]*change)

########################################################################

################### main function code block ###########################
# 
def main():

    print("Enter your desired Resistor Size: ")
    resistorStr = input()
    if (not isValid(resistorStr)): # Error
        main()
    multiplier = getMultiplier(resistorStr)
    if (multiplier == -1): # Error
        main()
    resistorNum = replaceSuffix(resistorStr)
    if (resistorNum == -1): # Error
        main()

    desiredResistor = multiplier*resistorNum
    resistorMin = desiredResistor*(1 - resistorTol/100) #Min value resistor could be
    standardResistor = calcResistor(resistorMin) #Finds standard resistor value closest to input
    potValue = desiredResistor-standardResistor # Finds difference between desired and standard values to be made up by potentiometer

    print("Closest standard resistor value: ")
    print(standardResistor)

    print("Potentiometer value: ") # Actual pot value required
    if (potValue >= 0):
        print(potValue)
    else:
        print(0)
    
    print("Recommended Standard Potentiometer: ") # 2x Pot value in standard, for convenience
    print(calcResistor(potValue*2))

    print("\n\n\n")

    main()

# startup code
def begin():
    print("Enter Resistor Tolerance to be used for all calculations, default is 5 (%): ")
    resistorTol = input()
    if (resistorTol == "\0" or resistorTol == "\n"):
        resistorTol = DEFAULT_TOL
        print("Default tolerance accepted")
    elif (not resistorTol.isdecimal()):
        print("Please enter valid Resistor Tolerance: ")
        begin()
    
    # runs main() 
    if __name__ == "__main__":
        main()
    else:
        print("Error")

begin()
