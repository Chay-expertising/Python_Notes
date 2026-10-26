import csv

# newline="" lets the csv module handle line endings itself
with open("data/people.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)      # first row = column names
    print("Header:", header)
    for row in reader:         # every row is a list of strings
        print(row)
