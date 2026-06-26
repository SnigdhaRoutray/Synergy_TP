import json

def read_csv_manual(file_path):
    rows = []
    with open(file_path, "r") as file:
        lines = file.readlines()
    if not lines:
        return rows
    header = lines[0].strip().split(",")
    if not header:
        return rows
    for line in lines[1:]:
        line = line.strip()
        values = line.split(",")
        if len(values) != len(header):
            continue
        row = dict(zip(header, values))
        rows.append(row)
    return rows

def convert_types(rows):
    valid_rows = []
    for row in rows:
        try:
            row["score"] = int(row["score"])
            row["submitted"] = row["submitted"].strip().lower() == "yes"
        except (ValueError, KeyError):
            continue
        valid_rows.append(row)
    return valid_rows

def calculate_summary(rows):
    if not rows:
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
    submitted = []
    missing = []
    for row in rows:
        if row["submitted"]:
            submitted.append(row)
        else:
            missing.append(row)
    average = round(sum(row["score"] for row in rows) / len(rows), 2)
    highest = rows[0]
    for row in rows:
        if row["score"] > highest["score"]:
            highest = row
    lowest = None
    if submitted:
        lowest = submitted[0]
        for row in submitted:
            if row["score"] < lowest["score"]:
                lowest = row
    domain_scores = {}
    for row in rows:
        domain = row["domain"]
        if domain not in domain_scores:
            domain_scores[domain] = []
        domain_scores[domain].append(row["score"])
    domain_average = {}
    for domain, scores in domain_scores.items():
        domain_average[domain] = round(sum(scores) / len(scores), 2)
    return {
        "total_students": len(rows),
        "submitted_students": len(submitted),
        "missing_submissions": len(missing),
        "average_score": average,
        "highest_scorer": highest["name"],
        "lowest_submitted_scorer": lowest["name"] if lowest else None,
        "domain_average_score": domain_average,
        "students_not_submitted": [row["name"] for row in missing],
        "students_below_5": [row["name"] for row in rows if row["score"] < 5]
    }

def write_json(data, output_path):
    with open(output_path, "w") as file:
        json.dump(data, file, indent=4)