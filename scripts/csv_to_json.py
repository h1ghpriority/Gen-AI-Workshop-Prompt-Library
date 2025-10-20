#!/usr/bin/env python3
import pandas as pd
import json, os, sys, glob

def convert_file(csv_path: str):
    df = pd.read_csv(csv_path)
    # Expect columns: category name, title, text
    missing = [c for c in ["category name", "title", "text"] if c not in df.columns]
    if missing:
        raise ValueError(f"{csv_path} missing columns: {missing}")

    result = {}
    for category, group in df.groupby("category name"):
        items = [{"title": r["title"], "text": r["text"]} for _, r in group.iterrows()]
        result[category] = items

    base = os.path.splitext(csv_path)[0]
    out_path = base + ".json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Wrote: {out_path}")

def main():
    # If a path/glob is provided, use it; otherwise default to prompts/*.csv
    pattern = sys.argv[1] if len(sys.argv) > 1 else "prompts/*.csv"
    files = glob.glob(pattern)
    if not files:
        print(f"No CSV files found for pattern: {pattern}")
        sys.exit(0)
    for p in files:
        convert_file(p)

if __name__ == "__main__":
    main()
