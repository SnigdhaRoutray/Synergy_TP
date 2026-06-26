import pandas as pd

REQUIRED_COLUMNS = [
    "student_id",
    "name",
    "domain",
    "attendance_percent",
    "score",
    "study_hours",
    "height_cm",
    "weight_kg",
    "submitted"
]

VALID_DOMAINS = {
    "ML",
    "Web",
    "Electronics",
    "Mechanical"
}

VALID_SUBMITTED = {
    True,
    False
}

def validate_cleaned_data(df):
    errors = []
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            errors.append(f"Missing column: {column}")
    if errors:
        for error in errors:
            print(error)
        return False
    if df["student_id"].duplicated().any():
        errors.append("Duplicate student IDs found.")
    numeric_columns = [
        "attendance_percent",
        "score",
        "study_hours",
        "height_cm",
        "weight_kg"
    ]
    for column in numeric_columns:
        try:
            pd.to_numeric(df[column])
        except ValueError:
            errors.append(f"{column} must be numeric.")
    if not df["attendance_percent"].between(0, 100).all():
        errors.append("Attendance values must be between 0 and 100.")
    domains = set(df["domain"].dropna())
    if not domains.issubset(VALID_DOMAINS):
        errors.append("Invalid domain values found.")
    submitted = set(df["submitted"].dropna())
    if not submitted.issubset(VALID_SUBMITTED):
        errors.append("Invalid submitted values found.")
    for column in REQUIRED_COLUMNS:
        if df[column].isnull().any():
            errors.append(f"Missing values found in {column}.")
    if errors:
        print("\nValidation Errors:\n")
        for error in errors:
            print("-", error)
        return False
    return True