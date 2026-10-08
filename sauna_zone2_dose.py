#!/usr/bin/env python3
"""Sauna protocol dosing check.

Counts 175F+ sessions in a sauna log and reports them against the
four-session minimum dose. A --compare mode prints sauna and Zone 2
weekly totals side by side.

CSV format: date,temperature_f,minutes with a header row.

Run the tests with: python3 -m doctest sauna_zone2_dose.py -v
"""

import argparse
import csv
import sys

MIN_TEMP_F = 175.0
MIN_SESSIONS = 4


def parse_rows(text):
    """Parse CSV text into (date, temp, minutes) tuples, skipping the header.

    >>> parse_rows("date,temperature_f,minutes\\n2026-01-05,178,25\\n2026-01-06,170,30\\n")
    [('2026-01-05', 178.0, 25.0), ('2026-01-06', 170.0, 30.0)]
    """
    rows = []
    reader = csv.reader(text.splitlines())
    for i, row in enumerate(reader):
        if not row or (i == 0 and row[0].strip().lower().startswith("date")):
            continue
        rows.append((row[0].strip(), float(row[1]), float(row[2])))
    return rows


def count_dose(rows, min_temp=MIN_TEMP_F):
    """Count sessions that cleared the minimum temperature.

    >>> count_dose([("a", 178.0, 25), ("b", 170.0, 30), ("c", 176.5, 20)])
    2
    """
    return sum(1 for _, temp, _ in rows if temp >= min_temp)


def dose_report(rows, min_temp=MIN_TEMP_F, min_sessions=MIN_SESSIONS):
    """Render the weekly dose verdict.

    >>> print(dose_report([("a", 178.0, 25), ("b", 170.0, 30)]))
    Sessions at or above 175.0F: 1 of 2 logged
    Minimum dose: 4 sessions. 3 more needed this week.
    >>> print(dose_report([("a", 178.0, 25)] * 4))
    Sessions at or above 175.0F: 4 of 4 logged
    Minimum dose met: 4 sessions.
    """
    hot = count_dose(rows, min_temp)
    lines = [
        "Sessions at or above {:.1f}F: {} of {} logged".format(min_temp, hot, len(rows))
    ]
    if hot >= min_sessions:
        lines.append("Minimum dose met: {} sessions.".format(min_sessions))
    else:
        lines.append(
            "Minimum dose: {} sessions. {} more needed this week.".format(
                min_sessions, min_sessions - hot
            )
        )
    return "\n".join(lines)


def total_minutes(path):
    with open(path, newline="") as f:
        rows = parse_rows(f.read())
    return sum(m for _, _, m in rows), len(rows)


def main(argv=None):
    p = argparse.ArgumentParser(description="Sauna protocol dosing check")
    p.add_argument("sauna_csv", help="sauna session log: date,temperature_f,minutes")
    p.add_argument("--compare", metavar="ZONE2_CSV", help="Zone 2 log to compare against")
    args = p.parse_args(argv)

    with open(args.sauna_csv, newline="") as f:
        rows = parse_rows(f.read())
    print("== Sauna ==")
    print(dose_report(rows))

    if args.compare:
        z2_min, z2_n = total_minutes(args.compare)
        s_min = sum(m for _, _, m in rows)
        print("== Comparison ==")
        print("Sauna: {} sessions, {} minutes".format(len(rows), int(s_min)))
        print("Zone 2: {} sessions, {} minutes".format(z2_n, int(z2_min)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
