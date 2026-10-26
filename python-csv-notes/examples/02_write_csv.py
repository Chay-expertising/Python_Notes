import csv

# "w" creates the file, or overwrites it if it exists
with open("output/written.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])                  # one row
    writer.writerows([["Asha", 25], ["Ravi", 31]])    # many rows

with open("output/written.csv", encoding="utf-8") as f:
    print(f.read())
