import csv

# Append a row without writing the header again
with open("output/log.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["name", "age"])           # create with header
with open("output/log.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["Meera", 29])             # append only

# Count data rows, excluding the header
with open("data/people.csv", newline="", encoding="utf-8") as f:
    count = sum(1 for _ in csv.reader(f)) - 1
print("Data rows:", count)

print("---")

# Error handling
for path in ["data/missing.csv", "data/people.csv"]:
    try:
        with open(path, newline="", encoding="utf-8") as f:
            print(f"{path}: {len(list(csv.reader(f)))} rows read")
    except FileNotFoundError:
        print(f"{path}: file not found")
    except UnicodeDecodeError:
        print(f"{path}: wrong encoding, try utf-8-sig or cp1252")
    except csv.Error as e:
        print(f"{path}: malformed CSV ({e})")
