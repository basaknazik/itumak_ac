#!/usr/bin/env python3
"""
Pulls the latest rows from the published Google Sheet CSV and appends only
the NEW ones (by timestamp) to data/responses.csv, tracking what's already
been seen in data/seen.json.

This script never deletes or edits existing rows in responses.csv — that's
done by hand when reviewing the Pull Request this produces (edit the diff
directly in GitHub's PR review UI, then merge to approve or close to
reject). This keeps the public site's data file as the single source of
truth for what's actually published, while the raw Google Sheet can stay
messy/unmoderated.

Usage: python3 scripts/sync_responses.py
Exit code 0 with no changes if there's nothing new (workflow just skips
opening a PR in that case). Prints a one-line summary to stdout either way.
"""
import csv
import io
import json
import os
import sys
import urllib.request

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTpatDO_gh8in_zmZA_yra0L6NA3HeYm6Lyax98h91iGtFQyHC381mlEWgXAb4QxWn3DW_k5MSIYbto/pub?output=csv"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_PATH = os.path.join(ROOT, "data", "responses.csv")
SEEN_PATH = os.path.join(ROOT, "data", "seen.json")


def fetch_csv_rows():
    req = urllib.request.Request(CSV_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    return list(csv.reader(io.StringIO(raw)))


def load_seen():
    if not os.path.exists(SEEN_PATH):
        return {"seen_timestamps": [], "note": ""}
    with open(SEEN_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_responses():
    if not os.path.exists(RESPONSES_PATH):
        return None, []
    with open(RESPONSES_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return None, []
    return rows[0], rows[1:]


def main():
    remote_rows = fetch_csv_rows()
    if not remote_rows:
        print("Sheet boş görünüyor, bir şey yapılmadı.")
        return

    remote_header, remote_data = remote_rows[0], remote_rows[1:]

    seen = load_seen()
    seen_ts = set(seen.get("seen_timestamps", []))

    existing_header, existing_data = load_responses()
    header = existing_header or remote_header

    new_rows = []
    for row in remote_data:
        if not row or not any(cell.strip() for cell in row):
            continue
        ts = row[0].strip()
        if not ts or ts in seen_ts:
            continue
        new_rows.append(row)
        seen_ts.add(ts)

    if not new_rows:
        print("Yeni yanıt yok.")
        return

    with open(RESPONSES_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in existing_data:
            writer.writerow(row)
        for row in new_rows:
            writer.writerow(row)

    seen["seen_timestamps"] = sorted(seen_ts)
    with open(SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"{len(new_rows)} yeni yanıt eklendi (PR olarak açılacak).")
    # also write a small summary file the workflow can use as the PR body
    summary_path = os.path.join(ROOT, "data", ".sync_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"{len(new_rows)} yeni anket yanıtı geldi ve onayınızı bekliyor.\n\n")
        f.write("Yeni satırlar:\n")
        for row in new_rows:
            preview = " | ".join(c.strip() for c in row[:5])
            f.write(f"- {preview}\n")
        f.write("\nBu PR'ı inceleyin: sorunlu/troll bir cevap görürseniz satırı diff üzerinden silin, ")
        f.write("gerekirse metni düzenleyin, sonra Merge edin. Onaylamıyorsanız PR'ı Close edin ")
        f.write("(satır responses.csv'ye hiç girmemiş olur, site hiçbir zaman göstermez).\n")


if __name__ == "__main__":
    sys.exit(main())
