import sys

from analyzer import (
    read_submissions,
    get_submitted_students,
    calculate_average_score,
    get_domain_wise_average,
    get_missing_submissions,
    write_summary,
)

def main() -> None:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    df = read_submissions(input_file)
    if df.empty:
        return
    submitted = get_submitted_students(df)
    missing = get_missing_submissions(df)
    summary = {
        "total_students": len(df),
        "submitted_students": len(submitted),
        "missing_submissions": len(missing),
        "average_score": calculate_average_score(df),
        "highest_scorer": submitted.loc[submitted["score"].idxmax(), "name"],
        "lowest_scorer": submitted.loc[submitted["score"].idxmin(), "name"],
        "domain_wise_average": get_domain_wise_average(df),
        "students_not_submitted": missing,
        "students_below_5": submitted[submitted["score"] < 5]["name"].tolist()
    }

    print("Total Students:", summary["total_students"])
    print("Submitted Students:", summary["submitted_students"])
    print("Missing Submissions:", summary["missing_submissions"])
    print("Average Score:", summary["average_score"])
    print("Highest Scorer:", summary["highest_scorer"])
    print("Missing Students:", summary["students_not_submitted"])

    write_summary(summary, output_file)

    print(f"Summary written to {output_file}")


if __name__ == "__main__":
    main()