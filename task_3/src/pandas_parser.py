import json
import pandas as pd

def read_csv_pandas(file_path):
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    if df.empty:
        return df
    required_columns = ["name", "domain", "task", "score", "submitted"]
    for column in required_columns:
        if column not in df.columns:
            return pd.DataFrame()
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df = df.dropna(subset=["score"])
    df["score"] = df["score"].astype(int)
    df["submitted"] = (
        df["submitted"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "yes"
    )
    return df

def calculate_summary_pandas(df):
    if df.empty:
        return {
            "total_students": 0,
            "submitted_students": 0,
            "missing_submissions": 0,
            "average_score": 0.0,
            "highest_scorer": None,
            "lowest_submitted_scorer": None,
            "domain_average_score": {},
            "students_not_submitted": [],
            "students_below_5": []
        }
    submitted = df[df["submitted"]]
    missing = df[~df["submitted"]]
    domain_average = {}
    grouped = df.groupby("domain")["score"].mean()
    for domain, score in grouped.items():
        domain_average[domain] = round(score, 2)
    summary = {
        "total_students": len(df),
        "submitted_students": len(submitted),
        "missing_submissions": len(missing),
        "average_score": round(df["score"].mean(), 2),
        "highest_scorer": df.loc[df["score"].idxmax(), "name"],
        "lowest_submitted_scorer": submitted.loc[submitted["score"].idxmin(), "name"] if not submitted.empty else None,
        "domain_average_score": domain_average,
        "students_not_submitted": missing["name"].tolist(),
        "students_below_5": df[df["score"] < 5]["name"].tolist()
    }
    return summary

def write_json(data, output_path):
    with open(output_path, "w") as file:
        json.dump(data, file, indent=4)