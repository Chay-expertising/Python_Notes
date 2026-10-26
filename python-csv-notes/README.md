# CSV File Handling in Python: Study Notes

Every example in this file was run, and the output shown is the real output.
The code lives in `examples/`, and the sample data lives in `data/people.csv`.

```
data/people.csv
name,age,city,score
Asha,25,Chennai,88.5
Ravi,31,Madurai,
Meera,17,Coimbatore,92
Karthik,45,Chennai,71.25
```

Run any example from the project folder, for example `python3 examples/01_read_csv.py`.

---

## 1. Reading a CSV: `csv.reader`

A CSV file is plain text. Each line is a row, and commas separate the fields.
The `csv` module is part of the standard library, so no install is needed.

```python
import csv

with open("data/people.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)      # first row = column names
    print("Header:", header)
    for row in reader:         # every row is a list of strings
        print(row)
```

Output:

```
Header: ['name', 'age', 'city', 'score']
['Asha', '25', 'Chennai', '88.5']
['Ravi', '31', 'Madurai', '']
['Meera', '17', 'Coimbatore', '92']
['Karthik', '45', 'Chennai', '71.25']
```

**Points to remember**

- `next(reader)` reads the header and moves past it.
- Every value is a **string**, including `'25'`. Convert values yourself.
- An empty cell becomes `''`, not `None`.
- `newline=""` tells the csv module to handle line endings itself. Without it, you can get blank lines between rows on Windows.

---

## 2. Writing a CSV: `csv.writer`

```python
import csv

with open("output/written.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])                  # one row
    writer.writerows([["Asha", 25], ["Ravi", 31]])    # many rows

with open("output/written.csv", encoding="utf-8") as f:
    print(f.read())
```

Output:

```
name,age
Asha,25
Ravi,31
```

**Points to remember**

- `"w"` creates the file, or **overwrites it** if it already exists.
- `writerow()` writes one row. `writerows()` writes a list of rows.
- Numbers are converted to text automatically.

---

## 3. Column names with `DictReader` and `DictWriter`

Using `row[1]` is hard to read and breaks if the column order changes.
These classes use the header names instead.

```python
import csv

with open("data/people.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], "is", row["age"], "from", row["city"])

with open("output/dict_written.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Asha", "age": 25})
    writer.writerow({"age": 31, "name": "Ravi"})   # key order doesn't matter

with open("output/dict_written.csv", encoding="utf-8") as f:
    print(f.read())
```

Output:

```
Asha is 25 from Chennai
Ravi is 31 from Madurai
Meera is 17 from Coimbatore
Karthik is 45 from Chennai
name,age
Asha,25
Ravi,31
```

**Points to remember**

- Each row from `DictReader` is a dictionary: `row["name"]`.
- `DictWriter` needs `fieldnames` so it knows the column order.
- `writeheader()` writes the header row. Call it once.

---

## 4. Delimiters: commas, semicolons, tabs

Not every CSV uses commas. Semicolons are common in European locales, and tabs give you TSV files.

```python
import csv
import io

semi = "name;age\nAsha;25\nRavi;31\n"
for row in csv.reader(io.StringIO(semi), delimiter=";"):
    print(row)
```

Output:

```
['name', 'age']
['Asha', '25']
['Ravi', '31']
```

Use `delimiter="\t"` for tab-separated files.

---

## 5. Quoting: fields with commas, quotes or newlines

The csv module adds quotes when a field needs them, and doubles any quote inside a field.

```python
import csv
import io

buffer = io.StringIO()
writer = csv.writer(buffer)
writer.writerow(['He said "hi"', "a,b", "two\nlines", "plain"])
print(buffer.getvalue())

buffer = io.StringIO()
csv.writer(buffer, quoting=csv.QUOTE_ALL).writerow(["x", 1, 2.5])
print(buffer.getvalue())
```

Output:

```
"He said ""hi""","a,b","two
lines",plain

"x","1","2.5"
```

**Quoting options**

| Constant | What it does |
|---|---|
| `QUOTE_MINIMAL` (default) | Quotes only fields that need it |
| `QUOTE_ALL` | Quotes every field |
| `QUOTE_NONNUMERIC` | Quotes text fields; numbers are read back as floats |
| `QUOTE_NONE` | Never quotes; needs an `escapechar` |

---

## 6. Encoding

- Use `encoding="utf-8"` as the default.
- Files saved from Excel may start with a hidden byte-order mark (BOM). Open them with `encoding="utf-8-sig"` to remove it. Without this, the first column name can appear as `﻿name`.
- Older Windows files may need `encoding="cp1252"`.

---

## 7. Type conversion and empty cells

```python
import csv

with open("data/people.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        age = int(row["age"])
        score = float(row["score"]) if row["score"] else None   # empty -> None
        print(f"{row['name']:<8} age={age:<3} score={score}")

with open("data/people.csv", newline="", encoding="utf-8") as f:
    scores = [float(r["score"]) for r in csv.DictReader(f) if r["score"]]
print("Average score:", round(sum(scores) / len(scores), 2))
```

Output:

```
Asha     age=25  score=88.5
Ravi     age=31  score=None
Meera    age=17  score=92.0
Karthik  age=45  score=71.25
Average score: 83.92
```

**Points to remember**

- Convert with `int()` or `float()`. These raise `ValueError` if the text isn't a number.
- Check for empty strings before converting. `float("")` raises an error.
- The average skips Ravi, whose score is empty.

---

## 8. Filtering rows into a new file

Read one row at a time, keep the rows you want, and write them out.

```python
import csv

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
```

Output:

```
name,age,city,score
Asha,25,Chennai,88.5
Ravi,31,Madurai,
Karthik,45,Chennai,71.25
```

Meera (17) is left out. `reader.fieldnames` reuses the original header, so you don't have to type it again.

---

## 9. Appending, counting rows, and error handling

```python
import csv

# Create with a header, then append without repeating it
with open("output/log.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["name", "age"])
with open("output/log.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["Meera", 29])

# Count data rows, excluding the header
with open("data/people.csv", newline="", encoding="utf-8") as f:
    count = sum(1 for _ in csv.reader(f)) - 1
print("Data rows:", count)

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
```

Output:

```
Data rows: 4
---
data/missing.csv: file not found
data/people.csv: 5 rows read
```

**Mode letters**

| Mode | Meaning |
|---|---|
| `"r"` | Read (default) |
| `"w"` | Write, overwriting the file |
| `"a"` | Append to the end of the file |

`people.csv` reports 5 rows because the header counts as one row.

---

## 10. Large files

`csv.reader` and `DictReader` read one row at a time, so memory use stays low. Avoid `list(reader)` on a very large file, because it loads every row into memory at once.

---

## Quick Reference

| Task | Code |
|---|---|
| Read rows as lists | `csv.reader(f)` |
| Read rows as dicts | `csv.DictReader(f)` |
| Write rows from lists | `csv.writer(f).writerow(...)` |
| Write rows from dicts | `csv.DictWriter(f, fieldnames=...)` |
| Use semicolons | `delimiter=";"` |
| Remove Excel BOM | `encoding="utf-8-sig"` |
| Append to a file | `open(path, "a", newline="")` |

## Practice

1. Print only the names of people in Chennai.
2. Write a file that contains only the people with a score above 80.
3. Find the oldest person and print their name.
4. Read `people.csv` with `delimiter=";"` after converting its commas to semicolons, and explain the result.
