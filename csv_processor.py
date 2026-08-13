import csv

def is_number(value):
    if value is None or value.strip() == "":
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False

def analyze_csv(file_path):
    with open(file_path,mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames or []

    if not rows:
        return None, []

    numeric_columns = []
    for column in headers:
        values = [row[column] for row in rows if row[column] is not None]
        non_blank = [v for v in values if v.strip() != ""]
        if non_blank and all(is_number(v) for v in non_blank):
            numeric_columns.append(column)

    if not numeric_columns:
        return None, []

    results = {}
    for column in numeric_columns:
        values = [
            float(row[column])
            for row in rows
            if row[column]is not None and row[column].strip() != ""
        ]

        if values:
            total_sum = sum(values)
            results[column] = {
                "Average": sum(values) / len(values),
                "Minimum": min(values),
                "Maximum": max(values),
                "Sum": total_sum,
        }

    return results, numeric_columns
