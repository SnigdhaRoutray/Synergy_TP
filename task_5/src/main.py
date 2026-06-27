import os
import sys

from visualize import (
    load_cleaned_data,
    plot_domain_average_score,
    plot_attendance_vs_score,
    plot_submission_status_count,
    write_plot_summary,
)

def main():
    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    os.makedirs(output_folder, exist_ok=True)
    df = load_cleaned_data(input_file)
    plot_domain_average_score(df, output_folder)
    plot_attendance_vs_score(df, output_folder)
    plot_submission_status_count(df, output_folder)
    write_plot_summary(output_folder)

if __name__ == "__main__":
    main()