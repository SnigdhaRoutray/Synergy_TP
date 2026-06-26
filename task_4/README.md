# Task 4: Messy CSV Cleaning

## Objective

The objective of this task is to clean a messy CSV dataset using pandas and generate a cleaned dataset, validation checks, summary reports, and a cleaning report. Such data cleaning before performing data analysis or machine learning.

---

## Folder Structure

```text
task_4/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── messy_students.csv
│
├── output/
│   ├── cleaned_students.csv
│   ├── cleaning_report.md
│   ├── summary_before.json
│   └── summary_after.json
│
└── src/
    ├── clean_data.py
    ├── validate_data.py
    └── main.py
```

---

## Required Packages

* Python 3.x
* pandas
* word2number

Install the required packages using:

```bash
pip install -r task_4/requirements.txt
```

---

## Setup Instructions

1. Clone the repository.
2. Install the required packages.
3. Ensure the input dataset is present at:

```text
task_4/data/messy_students.csv
```

4. Run the program from the root directory of the repository.

---

## Run Command

```bash
python task_4/src/main.py task_4/data/messy_students.csv task_4/output/cleaned_students.csv
```

---

## Expected Output Files

After successful execution, the following files will be generated inside the `task_4/output/` directory:

```text
task_4/output/
├── cleaned_students.csv
├── cleaning_report.md
├── summary_before.json
└── summary_after.json
```

---

## Implementation Logic

### Data Loading

* Loads the messy CSV dataset using pandas.
* Generates an initial summary before cleaning.

### Data Cleaning

The following cleaning steps are performed:

* Removes duplicate rows.
* Standardizes domain names.
* Converts attendance values to numeric percentages.
* Converts scores into numeric values.
* Converts study hours into numeric values.
* Converts heights into centimeters.
* Converts weights into kilograms.
* Standardizes submitted values into boolean values.
* Handles missing values using median imputation for numeric columns.
* Replaces invalid attendance values using the median of valid attendance values.

### Data Validation

The cleaned dataset is validated to ensure:

* Student IDs are unique.
* Attendance values are numeric and between 0 and 100.
* Score values are numeric.
* Study hour values are numeric.
* Height values are numeric.
* Weight values are numeric.
* Submitted values are consistent.
* Domain names contain only valid categories.
* Critical columns contain no missing values.

### Report Generation

The program generates:

* Summary before cleaning
* Summary after cleaning
* Cleaning report describing all cleaning decisions and modifications
* Final cleaned CSV dataset

---

## Cleaning Decisions

The following rules were applied during data cleaning:

* Duplicate rows were removed while keeping the first occurrence.

* Invalid attendance values (below 0 or above 100) were replaced using the median of valid attendance values.

* Missing numeric values were filled using the median of their respective columns.

* Heights were converted to centimeters.

* Weights were converted to kilograms.

* Domain names were standardized to:

  * ML
  * Web
  * Electronics
  * Mechanical

* Submitted values were standardized to True or False.

---

## Output Files

* `cleaned_students.csv`- Final cleaned dataset.
* `summary_before.json`- Dataset summary before cleaning.
* `summary_after.json`- Dataset summary after cleaning.
* `cleaning_report.md`- Cleaning decisions and modifications made during preprocessing.
