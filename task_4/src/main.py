import json
import sys
import pandas as pd

from clean_data import (
    load_data,
    generate_summary,
    remove_duplicates,
    standardize_domains,
    clean_attendance,
    clean_scores,
    clean_study_hours,
    clean_height,
    clean_weight,
    clean_submitted,
    handle_missing_values,
    save_cleaned_data,
    write_report
)

from validate_data import validate_cleaned_data

def write_json(data, output_path):
    with open(output_path, "w") as file:
        json.dump(data, file, indent=4)

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    df = load_data(input_file)
    summary_before = generate_summary(df)
    write_json(
        summary_before,
        "task_4/output/summary_before.json"
    )
    attendance = (
        df["attendance_percent"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    attendance = pd.to_numeric(
        attendance,
        errors="coerce"
    )
    report = {
        "duplicates_removed": int(df.duplicated().sum()),
        "attendance_missing": int(
            attendance.isna().sum()
        ),
        "attendance_invalid": int(
            ((attendance < 0) | (attendance > 100)).sum()
        ),
        "score_missing": int(
            df["score"].isna().sum()
        ),
        "study_missing": int(
            df["study_hours"].isna().sum()
        ),
        "height_missing": int(
            df["height"].isna().sum()
        ),
        "weight_missing": int(
            df["weight"].isna().sum()
        )
    }
    df = remove_duplicates(df)
    df = standardize_domains(df)
    df = clean_attendance(df)
    df = clean_scores(df)
    df = clean_study_hours(df)
    df = clean_height(df)
    df = clean_weight(df)
    df = clean_submitted(df)
    df = handle_missing_values(df)
    if not validate_cleaned_data(df):
        print("Validation failed.")
        return
    save_cleaned_data(
        df,
        output_file
    )
    summary_after = generate_summary(df)
    write_json(summary_after,"task_4/output/summary_after.json")
    write_report("task_4/output/cleaning_report.md",report)

if __name__ == "__main__":
    main()