import os
import pandas as pd
import matplotlib.pyplot as plt

def load_cleaned_data(file_path: str):
    return pd.read_csv(file_path)

def plot_domain_average_score(df, output_path: str) -> None:
    domain_average = df.groupby("domain")["score"].mean()
    plt.figure(figsize=(6, 4))
    domain_average.plot(kind="bar")
    plt.title("Average Score by Domain")
    plt.xlabel("Domain")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "domain_average_score.png"))
    plt.close()

def plot_attendance_vs_score(df, output_path: str) -> None:
    plt.figure(figsize=(6, 4))
    plt.scatter(df["attendance_percent"], df["score"])
    plt.title("Attendance Percentage vs Score")
    plt.xlabel("Attendance Percentage")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "attendance_vs_score.png"))
    plt.close()

def plot_submission_status_count(df, output_path: str) -> None:
    submission_count = df["submitted"].value_counts()
    plt.figure(figsize=(6, 4))
    submission_count.plot(kind="bar")
    plt.title("Submission Status Count")
    plt.xlabel("Submission Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "submission_status_count.png"))
    plt.close()

def write_plot_summary(output_path: str) -> None:
    summary = """# Plot Summary

## domain_average_score.png

This bar chart shows the average score for each domain.
It helps compare the overall performance of different domains.
Higher bars represent higher average scores.

## attendance_vs_score.png

This scatter plot shows the relationship between attendance percentage and score.
Each point represents one student.
It helps observe whether attendance is related to student scores.

## submission_status_count.png

This bar chart shows the number of students who submitted and did not submit.
It provides a quick comparison of the submission status.
The taller bar represents the more common submission status.
"""
    summary_path = os.path.join(output_path, "plot_summary.md")
    with open(summary_path, "w") as file:
        file.write(summary)