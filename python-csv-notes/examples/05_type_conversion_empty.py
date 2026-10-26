import csv

# Every value from a CSV is a string, so convert what you need
with open("data/people.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        age = int(row["age"])
        score = float(row["score"]) if row["score"] else None   # empty -> None
        print(f"{row['name']:<8} age={age:<3} score={score}")

print("---")

# Average of the non-empty scores
with open("data/people.csv", newline="", encoding="utf-8") as f:
    scores = [float(r["score"]) for r in csv.DictReader(f) if r["score"]]
print("Average score:", round(sum(scores) / len(scores), 2))
