import json
import os
import pandas as pd

def read_submissions(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)

        df["score"] = pd.to_numeric(df["score"])
        return df
    except FileNotFoundError:
        print("Error: File not found.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
        return pd.DataFrame()
    except ValueError:
        print("Error: Invalid score values found.")
        return pd.DataFrame()


def get_submitted_students(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["submitted"].str.lower() == "yes"]


def calculate_average_score(df: pd.DataFrame) -> float:
    submitted = get_submitted_students(df)
    if submitted.empty:
        return 0.0
    return round(submitted["score"].mean(), 2)

def get_domain_wise_average(df: pd.DataFrame) -> dict[str, float]:
    submitted = get_submitted_students(df)
    domain_avg = submitted.groupby("domain")["score"].mean()
    domain_avg = domain_avg.round(2)
    return domain_avg.to_dict()


def get_missing_submissions(df: pd.DataFrame) -> list[str]:
    missing = df[df["submitted"].str.lower() == "no"]
    return missing["name"].tolist()

def write_summary(summary: dict, output_path: str) -> None:
    folder = os.path.dirname(output_path)
    os.makedirs(folder, exist_ok=True)
    with open(output_path, "w") as file:
        json.dump(summary, file, indent=4)