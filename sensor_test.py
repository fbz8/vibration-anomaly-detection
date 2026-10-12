with open("demofile.csv", "w") as f :
    f.write("x,y,z\n")

    f.write("10, 25 , 31\n")
    f.write("13, 14 , 11\n")
    f.write("11, 0.5 , 1\n")
    f.write("1, 55 , 41\n")
    f.write("100, 215 , 61\n")
    f.write("105, 205 , 310\n")
    f.write("104, 95 , 41\n")
    f.write("47, 98 , 55\n")
    f.write("0.4, 5 , 3\n")
    f.write("106, 75 , 32\n")
with open("demofile.csv", "r") as f :
    print(f.read())
with open("demofile.csv", "r") as f :
    lines = f.readlines()
x_Values = []

for line in lines[1:] :
    values = line.strip().split(",")
    x =float(values[0])
    x_Values.append(x)
average = sum(x_Values) / len(x_Values)
print("Average x :" , average)   
normal_value = 50
tolerance = 10

if abs(average - normal_value) <= tolerance:
    print("Normal")
else:
    print("Abnormal")

