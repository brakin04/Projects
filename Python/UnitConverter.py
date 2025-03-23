class UnitConverter:

    # Initialize lists of units and conversion values
    lengthConv = [[ 1, 3.28084, 39.3701, 1.09361, 0.000621371, 0.001, 100, 1000, 0.000539957, 1.057e-16, 6.6846e-12, 3.24078e-17],
                    [ 0.3048, 1, 12, (1/3), (1/5280), 0.0003048, 30.48, 304.8, 0.000164579, 3.2217e-17, 2.0375e-12, 9.8779e-18],
                    [ 0.0254, (1/12), 1, ((1/12)/3), ((1/12)/5280), 0.0000254, 2.54, 25.4, 0.000013715, 2.6848e-18, 1.6979e-13, 8.2316e-19],
                    [ 0.9144, 3, 36, 1, (3/5280), 0.0009144, 91.44, 914.4, 0.000493737, 9.6652e-17, 6.1124e-12, 2.9634e-17],
                    [ 1609.34, 5280, 63360, 1760, 1, 1.60934, 160934, 1609344, 0.868976, 1.7011e-13, 1.0758e-8, 5.2155e-14],
                    [ 1000, 3280.84, 39370.1, 1093.61, 0.621371, 1, 100000, 1000000, 0.539957, 1.057e-13, 6.6846e-9, 3.2408e-14],
                    [ 0.01, 0.0328084, 0.393701, 0.0109361, 0.00000621371, 0.00001, 1, 10, 0.00000539957, 1.057e-18, 6.6846e-14, 3.2408e-19],
                    [ 0.001, 0.00328084, 0.0393701, 0.00109361, 0.000000621371, 0.000001, 0.1, 1, 0.000000539957, 1.057e-19, 6.6846e-15, 3.2408e-20],
                    [ 1852, 6076.12, 72913.4, 2025.37, 1.15078, 1.852, 185200, 1852000, 1, 1.9576e-13, 1.238e-8, 6.0019e-14],
                    [ 9.461e+15, 3.104e+16, 3.725e+17, 1.035e+16, 5.879e+12, 9.461e+12, 9.461e+17, 9.461e+18, 5.108e+12, 1, 63241.1, 0.306601],
                    [1.496e+11, 4.908e+11, 5.98e+12, 1.636e+11, 9.296e+7, 1.496e+8, 1.496e+13, 1.496e+14, 8.078e+7, 1.58125e-5, 1, 4.84184e-6],
                    [3.086e+16, 1.012e+17, 1.215e+18, 3.375e+16, 1.917e+13, 3.086e+13, 3.086e+18, 3.086e+19, 1.666e+13, 3.26156, 206265, 1]]
    lengths = ["Meters", "Feet", "Inches", "Yards", "Miles", "Kilometers", "Centimeters", "Millimeters", "Nautical miles", "Light years", "Astronomical units", "Parsecs"]
    volumeConv = [[ 1, 0.264172, 1.05669, 2.113376, 4.226753, 33.81402, 67.628, 202.884, 0.001, 0.0353147, 61.0237, 0.001308, 1000],
                    [ 3.78541, 1, 4, 8, 16, 128, 256, 768, 0.00378541, 0.133681, 231, 0.004951, 3785.412],
                    [ 0.946353, 0.25, 1, 2, 4, 32, 64, 192, 0.000946353, 0.0334201, 57.75, 0.001238, 946.353],
                    [ 0.473176, 0.125, 0.5, 1, 2, 16, 32, 96, 0.000473176, 0.0167101, 28.875, 0.000619, 473.176],
                    [ 0.236588, 0.0625, 0.25, 0.5, 1, 8, 16, 48, 0.000236588, 0.00847552, 14.6457, 0.000309, 236.588],
                    [ 0.0295735, 0.0078125, 0.03125, 0.0625, 0.125, 1, 2, 6, 0.0000295735, 0.00104438, 1.80469, 0.0000386807, 29.57353],
                    [ 0.0147868, 0.00390625, 0.015625, 0.03125, 0.0625, 0.5, 1, 3, 0.0000147868, 0.00052219, 0.902344, 0.000019340358, 14.786765],
                    [ 0.00492892, 0.00130208, 0.00520833, 0.0104167, 0.0208333, (1/6), 0.333333, 1, 0.00000492892, 0.000174063, 0.300781, 0.000006446786, 4.928922],
                    [ 1000, 264.172, 1056.68821, 2113.380, 4226.7528, 33814.023, 67628.045, 202884, 1, 35.3147, 61023.7, 1.307951, 1000000],
                    [ 28.3168, 7.48052, 29.9221, 59.8442, 117.987, 957.506, 1915.01, 5745.04, 0.0283168, 1, 1728, 0.037037, 28316.8],
                    [ 0.0163871, 0.004329, 0.017316, 0.034632, 0.0682794, 0.554113, 1.10823, 3.32468, 0.0000163871, 0.000578704, 1, 0.000021433, 16.3871],
                    [ 764.554858, 201.974026, 807.896104, 1615.792208, 3231.584416, 25852.675325, 51705.350649, 155116, 0.764555, 27, 46656, 1, 764555], 
                    [ 0.001, 0.000264172, 0.00105669, 0.00211338, 0.00422675, 0.033814, 0.067628, 0.202884, 0.000001, 3.5315e-5, 0.0610237, 0.000001308, 1]]
    volumes = ["Liters", "Gallons", "Quarts", "Pints", "Cups", "Ounces", "Tablespoons", "Teaspoons", "Cubic meters", "Cubic feet", "Cubic inches", "Cubic yards", "Mililiters"]
    weightsConv = [[ 1, 2.204623, 35.273962, 1000, 1000000, 0.001102, 0.001, 0.157473, 5000, 15432.358],
                    [ 0.453592, 1, 16, 453.5924, 453592.4, 0.0005, 0.000453592, 0.0714286, 2267.96, 7000],
                    [ 0.0283495, 0.0625, 1, 28.3495, 28349.5, 0.00003125, 0.0000283495, 0.00446429, 141.7476, 437.5],
                    [ 0.001, 0.00220462, 0.035274, 1, 1000, 0.00000110231, 0.000001, 0.000157473, 5, 15.4324],
                    [ 0.000001, 0.00000220462, 0.000035274, 0.001, 1, 1.10231e-9, 1e-9, 1.57473e-7, 0.005, 0.0154324],
                    [ 907.185, 2000, 32000, 907185, 907184740, 1, 0.907185, 142.857, 4535924, 14000000],
                    [ 1000, 2204.623, 35273.96, 1000000, 1000000000, 1.10231, 1, 157.473, 5000000, 15432358],
                    [ 6.350293, 14, 224, 6350.293, 6350293, 0.007, 0.00635, 1, 31751.5, 98000],
                    [ 0.0002, 0.000440925, 0.00705479, 0.2, 200, 2.20462e-7, 2e-7, 0.0000314946, 1, 3.086472],
                    [ 0.0000647989, 0.000142857, 0.00228571, 0.0647989, 64.7989, 7.142857e-8, 6.47989e-8, 0.0000102041, 0.323995, 1]]
    weights = ["Kilograms", "Pounds", "Ounces", "Grams", "Milligrams", "Tons", "Tonnes", "Stones", "Carats", "Grains"]
    temperatures = ["Celsius", "Fahrenheit", "Kelvin", "Rankine"]

    # Initial method
    def convert(self):
        entry = ""
        print("1. Length\n2. Volume\n3. Weight\n4. Temperature")
        entry = input("Enter your choice: ")
        # Try to cast to int until it works
        while True:
            try:
                choice = int(entry)
                if choice < 1 or choice > 4:
                    entry = input("Enter a number between 1 and 4: ")
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-4: ")
        # Route to right method
        if choice == 1:
            self.length()
        elif choice == 2:
            self.volume()
        elif choice == 3:
            self.weight()
        elif choice == 4:
            self.temperature()

    # "Meters", "Feet", "Inches", "Yards", "Miles", "Kilometers", "Centimeters", "Millimeters", "Nautical miles", "Light years", "Astronomical units", "Parsecs"
    def length(self):
        entry = ""
        length = len(self.lengths)
        entry = input("\nEnter the first value: ")
        # Try to cast to float until it works
        while True:
            try:
                val = float(entry)
                break
            except ValueError:
                entry = input("Enter a number: ")
        for i in range(0, length):
            print(str(i+1) + ". " + self.lengths[i])
        entry = input("Choose it's unit: ")
        # Try to cast to int until it works
        while True:
            try:
                unit = int(entry)
                if unit < 1 or unit > 12:
                    entry = input("Type a number 1-{0}: ".format(length))
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-{0}: ".format(length))
        # What to convert to
        # for i in range(0, length):
        #     print(str(i+1) + ". " + self.lengths[i])
        entry = input("Choose the unit to convert to: ")
        # Try to cast to int until it works
        while True:
            try:
                unit2 = int(entry)
                if unit2 < 1 or unit2 > 12:
                    entry = input("Type a number 1-{0}: ".format(length))
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-{0}: ".format(length))
        # Return val * conversion factor
        valfinal = val * self.lengthConv[unit-1][unit2-1]
        # Print out the answer
        printUnit1 = self.lengths[unit-1]
        printUnit2 = self.lengths[unit2-1]
        print("{0} {1} is equal to {2} {3}".format(val, printUnit1, valfinal, printUnit2))

    # "Liters", "Gallons", "Quarts", "Pints", "Cups", "Ounces", "Tablespoons", "Teaspoons", "Cubic meters", "Cubic feet", "Cubic inches", "Cubic yards", "Fluid Ounces", "Mililiters"
    def volume(self):
        entry = ""
        length = len(self.volumes)
        entry = input("\nEnter the first value: ")
        # Try to cast to float until it works
        while True:
            try:
                val = float(entry)
                break
            except ValueError:
                entry = input("Enter a number: ")
        # Print options
        for i in range(0, length):
            print(str(i+1) + ". " + self.volumes[i])
        # Ask for unit and try to cast to int until it works
        entry = input("Enter it's unit: ")
        while True:
            try:
                unit = int(entry)
                if unit < 1 or unit > length:
                    entry = input("Type a number 1-{0}: ".format(length))
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-{0}: ".format(length))
        # Ask for unit to convert to and try to cast to int until it works
        entry = input("Enter the unit to convert to: ")
        while True:
            try:
                unit2 = int(entry)
                if unit2 < 1 or unit2 > length:
                    entry = input("Type a number 1-{0}: ".format(length))
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-{0}: ".format(length))
        # Convert using table
        valfinal = val * self.volumeConv[unit-1][unit2-1]
        # Print out the answer
        printUnit1 = self.volumes[unit-1]
        printUnit2 = self.volumes[unit2-1]
        print("{0} {1} is equal to {2} {3}".format(val, printUnit1, valfinal, printUnit2))
        
    # "Kilograms", "Pounds", "Ounces", "Grams", "Milligrams", "US tons", "Metric tons", "Stones", "Carats", "Grains"
    def weight(self):
        entry = ""
        length = len(self.weights)
        entry = input("Enter the first value: ")
        # Try to cast to float until it works
        while True:
            try:
                val = float(entry)
                break
            except ValueError:
                entry = input("Enter a number: ")
        # Print options
        for i in range(0, length):
            print(str(i+1) + ". " + self.weights[i])
        # Ask for unit and try to cast to int until it works
        entry = input("Enter it's unit: ")
        while True:
            try:
                unit = int(entry)
                if unit < 1 or unit > length:
                    entry = input("Type a number 1-{0}: ".format(length))
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-{0}: ".format(length))
        # Ask for unit to convert to and try to cast to int until it works
        entry = input("Enter the unit to convert to: ")
        while True:
            try:
                unit2 = int(entry)
                if unit2 < 1 or unit2 > length:
                    entry = input("Type a number 1-{0}: ".format(length))
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-{0}: ".format(length))
        # Convert using table
        valfinal = val * self.weightsConv[unit-1][unit2-1]
        # Print out the answer
        printUnit1 = self.weights[unit-1]
        printUnit2 = self.weights[unit2-1]
        print("{0} {1} is equal to {2} {3}".format(val, printUnit1, valfinal, printUnit2))

    # "Celsius", "Fahrenheit", "Kelvin", "Rankine"
    def temperature(self):
        entry = ""
        length = len(self.temperatures)
        entry = input("\nEnter the first value: ")
        # Try to cast to float until it works
        while True:
            try:
                val = float(entry)
                break
            except ValueError:
                entry = input("Enter a number: ")
        # Print options
        for i in range(0, length):
            print(str(i+1) + ". " + self.temperatures[i])
        # Ask for unit and try to cast to int until it works
        entry = input("Enter it's unit: ")
        while True:
            try:
                unit = int(entry)
                if unit < 1 or unit > length:
                    entry = input("Type a number 1-{0}: ".format(length))
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-{0}: ".format(length))
        # Ask for unit to convert to and try to cast to int until it works
        entry = input("Enter the unit to convert to: ")
        while True:
            try:
                unit2 = int(entry)
                if unit2 < 1 or unit2 > length:
                    entry = input("Type a number 1-{0}: ".format(length))
                else:
                    break
            except ValueError:
                entry = input("Type a number 1-{0}: ".format(length))
        # Convert to Celcius
        val2 = 0
        if (unit == 1):
            val2 = val
        elif (unit == 2):
            val2 = (val - 32) * (5/9)
        elif (unit == 3):
            val2 = val - 273.15
        elif (unit == 4):
            val2 = (val - 491.67) * (5/9)
        # Convert to desired unit
        valfinal = 0
        if (unit2 == 1):
            valfinal = val2
        elif (unit2 == 2):
            valfinal = (val2 * (9/5)) + 32
        elif (unit2 == 3):
            valfinal = val2 + 273.15
        elif (unit2 == 4):
            valfinal = (val2 * (9/5)) + 491.67
        # Print out the answer
        printUnit1 = self.temperatures[unit-1]
        printUnit2 = self.temperatures[unit2-1]
        print("{0} {1} is equal to {2} {3}".format(val, printUnit1, valfinal, printUnit2))

    def another(self):
        while True:
            entry = input("Would you like to convert another value? (y/n): ")
            if entry == "Y" or entry == "y":
                return True
            elif entry == "N" or entry == "n":
                return False
            else:
                print("Enter either y or n")
        

if __name__ == '__main__':
    while True:
        uc = UnitConverter()
        uc.convert()
        if not uc.another():
            break
