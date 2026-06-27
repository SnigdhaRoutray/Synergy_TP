# Task 5: Matplotlib Visualization from Cleaned Data

## Objective

The objective of this task is to generate basic data visualizations from the cleaned student dataset created in Task 4. The program reads the cleaned CSV file, creates three different plots using matplotlib, saves them as PNG images, and generates a short summary explaining each visualization.

---

## Folder Structure

```text
task_5/
│
├── README.md
├── requirements.txt
├── src/
│   ├── visualize.py
│   └── main.py
└── output/
    ├── domain_average_score.png
    ├── attendance_vs_score.png
    ├── submission_status_count.png
    └── plot_summary.md
```

---

## Requirements

* Python 3.x
* pandas
* matplotlib

Install the required packages using:

```bash
pip install -r requirements.txt
```

---

## Input

The program uses the cleaned dataset generated in Task 4.

```text
task_4/output/cleaned_students.csv
```

---

## Output

After running the program, the following files are generated inside `task_5/output/`:

* `domain_average_score.png`
* `attendance_vs_score.png`
* `submission_status_count.png`
* `plot_summary.md`

---

## Visualizations Generated

### 1. Domain Average Score

* Bar chart
* Shows the average score for each domain.
* Helps compare the overall performance of different domains.

### 2. Attendance vs Score

* Scatter plot
* Shows the relationship between attendance percentage and score.
* Each point represents one student.

### 3. Submission Status Count

* Bar chart
* Shows the number of students who submitted and did not submit.
* Provides a quick comparison of submission status.

---

## Functions Implemented

* `load_cleaned_data(file_path)`
* `plot_domain_average_score(df, output_path)`
* `plot_attendance_vs_score(df, output_path)`
* `plot_submission_status_count(df, output_path)`
* `write_plot_summary(output_path)`

---

## Run

From the root directory of the repository, run:

```bash
python task_5/src/main.py task_4/output/cleaned_students.csv task_5/output
```
