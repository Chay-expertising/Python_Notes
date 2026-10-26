import csv
import io

# 1. Semicolon-separated text, read with a custom delimiter
semi = "name;age\nAsha;25\nRavi;31\n"
for row in csv.reader(io.StringIO(semi), delimiter=";"):
    print(row)

print("---")

# 2. Writing values that contain commas, quotes and newlines
buffer = io.StringIO()
writer = csv.writer(buffer)
writer.writerow(['He said "hi"', "a,b", "two\nlines", "plain"])
print(buffer.getvalue())

print("---")

# 3. QUOTE_ALL puts quotes around every field
buffer = io.StringIO()
csv.writer(buffer, quoting=csv.QUOTE_ALL).writerow(["x", 1, 2.5])
print(buffer.getvalue())
