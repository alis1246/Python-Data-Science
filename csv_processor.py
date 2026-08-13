import csv
from typing import Any

IGNORED_ID_COLUMNS = {
    "srno", "sr_no", "sr.no", "sr. no", "sno", "s_no", "s.no",
    "id", "student_id", "sid", "s_id", "stud_id", "emp_id", "e_id", "employee_id", "index", "slno", "sl_no"
}

def is_number(value: Any) -> bool:
    if value is None:
        return False
    val_str = str(value).strip()
    if not val_str:
        return False

    try:
        float(val_str)
        return True
    except ValueError:
        return False

def analyze_csv(file_path):
    try:
        with open(file_path,mode="r", newline="", encoding="utf-8-sig") as f:
            sample = f.read(2048)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample) if sample.strip() else "excel"

            reader = csv.DictReader(f, dialect=dialect)
            rows = list(reader)
            raw_headers = reader.fieldnames or []
    except Exception as e:
        raise RuntimeError(f"Unable to parse CSV file: {str(e)}")

    if not rows:
        return None, []

    numeric_columns = []
    for column in raw_headers:
        if not column:
            continue

        col_clean = column.strip().lower()

        if col_clean in IGNORED_ID_COLUMNS:
            continue

        values = [row.get(column) for row in rows if row.get(column) is not None]
        non_blank = [v.strip() for v in values if v.strip() != "" and isinstance(v, str)]

        if non_blank and all(is_number(v) for v in non_blank):
            numeric_columns.append(column)

    if not numeric_columns:
        return None, []

    results = {}
    for column in numeric_columns:
        parsed_values = [
            float(row[column])
            for row in rows
            if row.get(column) is not None and str(row[column]).strip() != ""
        ]

        if parsed_values:
            total_sum = sum(parsed_values)
            clean_col_name = column.strip()
            results[clean_col_name] = {
                "Average": total_sum / len(parsed_values),
                "Minimum": min(parsed_values),
                "Maximum": max(parsed_values),
                "Sum": total_sum,
        }

    clean_numeric_cols = [c.strip() for c in numeric_columns]
    return results, clean_numeric_cols
