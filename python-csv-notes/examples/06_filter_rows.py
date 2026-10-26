import csv

# Read rows, keep the ones that match, write them to a new file
with open("data/people.csv", newline="", encoding="utf-8") as src, \
     open("output/adults.csv", "w", newline="", encoding="utf-8") as dst:
    reader = csv.DictReader(src)
    writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        if int(row["age"]) >= 18:
            writer.writerow(row)

with open("output/adults.csv", encoding="utf-8") as f:
    print(f.read())
