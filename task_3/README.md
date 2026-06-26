# Task 3: Manual CSV Parser and Pandas Comparison

## Objective

The objective of this task is to manually parse a CSV file using Python file handling and compare the results with a pandas-based implementation. This shows how CSV data can be processed without relying on high-level libraries and also verifies that both approaches produce identical results.

---

## Folder Structure

```text
task_3/
│
├── README.md
├── data/
│   └── submissions.csv
├── output/
│   ├── manual_summary.json
│   ├── pandas_summary.json
│   └── comparison_report.md
└── src/
    ├── manual_parser.py
    ├── pandas_parser.py
    └── main.py
```

---

## Required Packages

* Python 3.x
* pandas

Install the required package using:

```bash
pip install -r task_3/requirements.txt
```

---

## Setup Instructions

1. Clone the repository.
2. Install the required packages.
3. Ensure the input CSV file is present at:

```text
task_3/data/submissions.csv
```

4. Run the program from the root directory of the repository.

---

## Run Command

```bash
python task_3/src/main.py task_3/data/submissions.csv
```

---

## Expected Output Files

After successful execution, the following files will be generated inside the `task_3/output/` directory:

```text
task_3/output/
├── manual_summary.json
├── pandas_summary.json
└── comparison_report.md
```

---

## Implementation Logic

### Manual Parser

* Reads the CSV file using Python's built-in `open()` function.
* Splits the header and each row manually.
* Converts each row into a dictionary.
* Converts the `score` column to integers.
* Converts the `submitted` column to boolean values.
* Ignores empty lines, malformed rows, and invalid data without crashing.
* Calculates the required summary statistics.
* Writes the summary to `manual_summary.json`.

### Pandas Parser

* Reads the same CSV file using pandas.
* Converts data types appropriately.
* Handles invalid numeric values and empty data.
* Calculates the same summary statistics.
* Writes the summary to `pandas_summary.json`.

### Comparison Report

The generated summaries from both implementations are compared. A comparison report is created indicating whether both outputs match exactly or whether differences were found.

---

## Summary generated

The program calculates:

* Total number of students
* Number of submitted students
* Number of missing submissions
* Average score
* Highest scorer
* Lowest scorer among submitted students
* Domain-wise average score
* Students who did not submit
* Students scoring below 5

---

## Edge Cases Handled

The implementation safely handles:

* Empty CSV files
* Empty lines
* Malformed rows with incorrect column counts
* Missing required fields
* Invalid score values
* Different capitalizations and extra spaces in the `submitted` column
