import csv

# DictReader: each row becomes a dict keyed by the header
with open("data/people.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], "is", row["age"], "from", row["city"])

# DictWriter: write dicts, with the header written first
with open("output/dict_written.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Asha", "age": 25})
    writer.writerow({"age": 31, "name": "Ravi"})   # key order doesn't matter

with open("output/dict_written.csv", encoding="utf-8") as f:
    print(f.read())
