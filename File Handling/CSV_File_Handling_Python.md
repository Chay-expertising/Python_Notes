# CSV File Handling in Python

## What is a CSV file?

A CSV file (Comma-Separated Values) is a plain text file that stores a table. Each line is one row, and commas separate the values in that row. Excel and Google Sheets can open CSV files, and Python's built-in `csv` module reads and writes them. No installation is needed.

Sample file used in every example, named `people.csv`:

```
name,age,city,score
Asha,25,Chennai,88.5
Ravi,31,Madurai,
Meera,17,Coimbatore,92
Karthik,45,Chennai,71.25
```

- The first line is the **header**, which gives the column names.
- Ravi's score is empty.

### Reading a CSV file (`csv.reader`)

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
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

Notes:
- `open()` opens the file. `with` closes it automatically when the block ends.
- `next(reader)` reads the header and moves past it.
- Every value is a **string**, even `'25'`.
- An empty cell comes back as `''`.
- `newline=""` prevents extra blank lines on Windows. Always include it.

### Writing a CSV file (`csv.writer`)

Mode `"w"` creates the file, or **overwrites** it if it already exists.

```python
import csv

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])                  # one row
    writer.writerows([["Asha", 25], ["Ravi", 31]])    # several rows

with open("output.csv", encoding="utf-8") as f:
    print(f.read())
```

Output:

```
name,age
Asha,25
Ravi,31
```

Notes:
- `writerow()` writes one row. `writerows()` writes a list of rows.
- Numbers are converted to text automatically.

### Reading rows as dictionaries (`DictReader`)

`row[1]` is hard to read, and it breaks if the columns move. `DictReader` uses the column names instead.

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], "is", row["age"], "from", row["city"])
```

Output:

```
Asha is 25 from Chennai
Ravi is 31 from Madurai
Meera is 17 from Coimbatore
Karthik is 45 from Chennai
```

### Writing rows as dictionaries (`DictWriter`)

```python
import csv

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()                              # writes: name,age
    writer.writerow({"name": "Asha", "age": 25})
    writer.writerow({"age": 31, "name": "Ravi"})      # key order doesn't matter

with open("output.csv", encoding="utf-8") as f:
    print(f.read())
```

Output:

```
name,age
Asha,25
Ravi,31
```

Notes:
- `fieldnames` sets the column order.
- Call `writeheader()` once, at the start.

### Other delimiters: semicolons and tabs

Not every CSV uses commas. Semicolons are common in European Excel files, and tabs make TSV files.

```python
import csv
import io

data = "name;age\nAsha;25\nRavi;31\n"
for row in csv.reader(io.StringIO(data), delimiter=";"):
    print(row)
```

Output:

```
['name', 'age']
['Asha', '25']
['Ravi', '31']
```

Notes:
- `io.StringIO` treats a string like a file, so this example needs no file on disk.
- For tabs, use `delimiter="\t"`.

### Quoting: values with commas, quotes, or line breaks

The `csv` module wraps such values in quotes automatically.

```python
import csv
import io

buffer = io.StringIO()
writer = csv.writer(buffer)
writer.writerow(['He said "hi"', "a,b", "two\nlines", "plain"])
print(buffer.getvalue())
```

Output:

```
"He said ""hi""","a,b","two
lines",plain
```

- `He said "hi"` is wrapped in quotes, and its inner quotes are doubled.
- `a,b` is wrapped, so its comma doesn't split it into two columns.

To quote every value, use `quoting=csv.QUOTE_ALL`:

```python
import csv
import io

buffer = io.StringIO()
csv.writer(buffer, quoting=csv.QUOTE_ALL).writerow(["x", 1, 2.5])
print(buffer.getvalue())
```

Output:

```
"x","1","2.5"
```

### Encoding: fixing strange characters

- Use `encoding="utf-8"` as the default.
- Excel sometimes adds a hidden marker at the start of a file. It makes the first column name show up as `﻿name`. Use `encoding="utf-8-sig"` to remove it.

```python
with open("people.csv", newline="", encoding="utf-8-sig") as f:
    ...
```

### Converting values and handling empty cells

Every value is a string, so convert numbers before doing math.

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        age = int(row["age"])
        score = float(row["score"]) if row["score"] else None   # empty becomes None
        print(f"{row['name']:<8} age={age:<3} score={score}")
```

Output:

```
Asha     age=25  score=88.5
Ravi     age=31  score=None
Meera    age=17  score=92.0
Karthik  age=45  score=71.25
```

Average score, skipping Ravi's empty one:

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    scores = [float(r["score"]) for r in csv.DictReader(f) if r["score"]]

print("Average score:", round(sum(scores) / len(scores), 2))
```

Output:

```
Average score: 83.92
```

Notes:
- `int()` and `float()` raise `ValueError` if the text isn't a number.
- Check for an empty string before converting, because `float("")` causes an error.

### Filtering rows into a new file

Read one row at a time, keep the rows you want, and write them out. This keeps people aged 18 or over.

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as src, \
     open("adults.csv", "w", newline="", encoding="utf-8") as dst:
    reader = csv.DictReader(src)
    writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        if int(row["age"]) >= 18:
            writer.writerow(row)

with open("adults.csv", encoding="utf-8") as f:
    print(f.read())
```

Output:

```
name,age,city,score
Asha,25,Chennai,88.5
Ravi,31,Madurai,
Karthik,45,Chennai,71.25
```

Notes:
- Meera (17) was left out.
- `reader.fieldnames` reuses the original header, so you don't retype the column names.

### Appending, counting rows, and handling errors

Mode `"a"` adds to the end of a file without erasing it:

```python
import csv

with open("log.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["name", "age"])           # create with a header

with open("log.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["Meera", 29])             # add one row
```

Count the data rows, not counting the header:

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    count = sum(1 for _ in csv.reader(f)) - 1

print("Data rows:", count)
```

Output:

```
Data rows: 4
```

Handle errors so the program doesn't crash:

```python
import csv

for path in ["missing.csv", "people.csv"]:
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
missing.csv: file not found
people.csv: 5 rows read
```

`people.csv` reports 5 rows because the header counts as one.

### Large files

`csv.reader` and `DictReader` read one row at a time, so they use little memory even on huge files. Avoid `list(reader)` on very large files, because it loads every row at once.

## Quick reference

| Task | Code |
|---|---|
| Read rows as lists | `csv.reader(f)` |
| Read rows as dictionaries | `csv.DictReader(f)` |
| Write rows from lists | `csv.writer(f).writerow(...)` |
| Write rows from dictionaries | `csv.DictWriter(f, fieldnames=[...])` |
| Semicolon separator | `delimiter=";"` |
| Remove Excel's hidden marker | `encoding="utf-8-sig"` |
| Add to end of file | `open(path, "a", newline="")` |
| Always include | `newline=""` |

| Mode | Meaning |
|---|---|
| `"r"` | Read (default) |
| `"w"` | Write, overwriting the file |
| `"a"` | Append to the end |

## Practice

1. Print only the names of people from Chennai.
2. Write a new file with only the people whose score is above 80.
3. Find the oldest person and print their name.
4. Create a semicolon-separated version of `people.csv`, then read it back with `delimiter=";"`.
