import json
import re
import pandas as pd
from word2number import w2n

DOMAIN_MAP = {
    "ml": "ML",
    "machine learning": "ML",
    "web": "Web",
    "web dev": "Web",
    "web development": "Web",
    "electronics": "Electronics",
    "mechanical": "Mechanical"
}

SUBMITTED_MAP = {
    "yes": True,
    "y": True,
    "true": True,
    "1": True,
    "no": False,
    "n": False,
    "false": False,
    "0": False
}

def load_data(file_path):
    return pd.read_csv(file_path)

def generate_summary(df):
    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum())
    }
    categorical = {}
    for column in df.select_dtypes(include="object").columns:
        categorical[column] = (
            df[column]
            .dropna()
            .unique()
            .tolist()
        )
    summary["unique_categorical_values"] = categorical
    return summary

def remove_duplicates(df):
    return df.drop_duplicates()

def standardize_domains(df):
    df["domain"] = (
        df["domain"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(DOMAIN_MAP)
    )
    return df

def clean_attendance(df):
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
    valid = attendance.between(0, 100)
    median = attendance[valid].median()
    attendance.loc[~valid] = median
    df["attendance_percent"] = attendance
    return df

def convert_word_number(value):
    if pd.isna(value):
        return None
    value = str(value).strip().lower()
    try:
        return float(value)
    except (ValueError, TypeError):
        try:
            return float(
                w2n.word_to_num(value)
            )
        except (ValueError, TypeError):
            return None

def clean_numeric_column(df, column):
    df[column] = (
        df[column]
        .apply(convert_word_number)
    )
    return df

def clean_scores(df):
    return clean_numeric_column(df, "score")

def clean_study_hours(df):
    return clean_numeric_column(df, "study_hours")

def extract_number(value):
    if pd.isna(value):
        return None
    value = str(value).strip().lower()
    number = re.findall(r"[\d.]+", value)
    if not number:
        return None
    return float(number[0])

def clean_height(df):
    heights = []
    for value in df["height"]:
        number = extract_number(value)
        if number is None:
            heights.append(None)
            continue
        value = str(value).lower()
        if "m" in value and "cm" not in value:
            number *= 100
        heights.append(number)
    df["height_cm"] = heights
    df = df.drop(columns=["height"])
    return df

def clean_weight(df):
    weights = []
    for value in df["weight"]:
        number = extract_number(value)
        weights.append(number)
    df["weight_kg"] = weights
    df = df.drop(columns=["weight"])
    return df

def clean_submitted(df):
    df["submitted"] = (
        df["submitted"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(SUBMITTED_MAP)
    )
    return df

def handle_missing_values(df):
    numeric_columns = [
        "attendance_percent",
        "score",
        "study_hours",
        "height_cm",
        "weight_kg"
    ]
    for column in numeric_columns:

        df[column] = df[column].fillna(
            df[column].median()
        )
    df["submitted"] = (
        df["submitted"]
        .fillna(False)
    )
    return df

def save_cleaned_data(df, output_path):
    df.to_csv(
        output_path,
        index=False
    )

def write_report(report_path, report):
    with open(report_path, "w") as file:
        file.write("Cleaning Report\n\n")
        file.write("Cleaning Decisions\n\n")
        file.write(f"- Removed {report['duplicates_removed']} duplicate row(s).\n")
        file.write(f"- Filled {report['attendance_missing']} missing attendance value(s).\n")
        file.write(f"- Corrected {report['attendance_invalid']} invalid attendance value(s).\n")
        file.write(f"- Filled {report['score_missing']} missing score value(s).\n")
        file.write(f"- Filled {report['study_missing']} missing study hour value(s).\n")
        file.write(f"- Filled {report['height_missing']} missing height value(s).\n")
        file.write(f"- Filled {report['weight_missing']} missing weight value(s).\n\n")
        file.write("Additional Cleaning Performed:\n\n")
        file.write("- Standardized domain names.\n")
        file.write("- Converted attendance to numeric percentages.\n")
        file.write("- Converted scores to numeric values.\n")
        file.write("- Converted study hours to numeric values.\n")
        file.write("- Converted heights to centimeters.\n")
        file.write("- Converted weights to kilograms.\n")
        file.write("- Standardized submitted values to True/False.\n")