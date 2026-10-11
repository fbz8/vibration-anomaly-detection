import math
import random
import csv

def make_reading(t, abnormal=False):
    amp = 3.0 if abnormal else 1.0
    freq = 12 if abnormal else 5
    noise = random.gauss(0, 0.3 if not abnormal else 0.8)

    x = amp * math.sin(2 * math.pi * freq * t) + noise
    return [round(t, 3), round(x, 3)]




NUM_ROWS = 50000


DT = 0.01


with open("normal.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["t", "x"])

    for i in range(NUM_ROWS):
        t = i * DT
        reading = make_reading(t, abnormal=False)
        writer.writerow(reading)


with open("abnormal.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["t", "x"])

    for i in range(NUM_ROWS):
        t = i * DT
        reading = make_reading(t, abnormal=True)
        writer.writerow(reading)

print("Finished generating both datasets.")
print(f"Normal readings: {NUM_ROWS}")
print(f"Abnormal readings: {NUM_ROWS}")