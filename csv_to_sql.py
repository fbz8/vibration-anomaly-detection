
import csv
import sqlite3

# 1. Connect to a database (creates it if it doesn't exist)
connection = sqlite3.connect("sensors.db")
cursor = connection.cursor()

# 2. Create the readings table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        x REAL,
        y REAL,
        z REAL
    )
""")

# Clear old data so rerunning the script won't duplicate rows
cursor.execute("DELETE FROM readings")

# 3. Read the CSV and insert every row into SQL
with open("demofile.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute(
            "INSERT INTO readings (x, y, z) VALUES (?, ?, ?)",
            (float(row["x"]), float(row["y"]), float(row["z"]))
        )

# Save the inserted rows
connection.commit()

# 4. Calculate the average of x
cursor.execute("SELECT AVG(x) FROM readings")
average_x = cursor.fetchone()[0]

# 5. Count rows where x is above 50
cursor.execute("SELECT COUNT(*) FROM readings WHERE x > 50")
count_above_50 = cursor.fetchone()[0]

# 6. Display the results
print("Average x:", average_x)
print("Rows where x > 50:", count_above_50)

# 7. Close the database connection
connection.close()