#!/usr/bin/env python3
"""
export_inscriptions.py - Εξάγει τον πίνακα inscriptions_table.md
σε CSV, JSON, SQLite και παράγει στατιστικά.

Χρήση:
    python export_inscriptions.py
    python export_inscriptions.py --format csv|json|sqlite|stats
    python export_inscriptions.py --input myfile.md
"""

import csv, json, re, sqlite3, argparse, os
from collections import Counter

COLUMNS = [
    'name', 'support', 'site', 'findspot', 'scribe', 'date',
    'ascii_transcription', 'unicode_transcription', 'reference', 'commentary'
]


def load_markdown(filepath):
    rows = []
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line.startswith('|') or line.startswith('|---'):
            continue
        # Σπάμε με | και αφαιρούμε ΜΟΝΟ τα εξωτερικά κενά στοιχεία
        cells = [c.strip() for c in line.split('|')]
        if cells and cells[0] == '':
            cells = cells[1:]
        if cells and cells[-1] == '':
            cells = cells[:-1]
        # Παράλειψε header
        if cells and cells[0] == 'Name':
            continue
        if len(cells) < 6:
            continue
        # Συμπλήρωσε με κενά αν λείπουν στήλες (π.χ. κενό reference)
        while len(cells) < len(COLUMNS):
            cells.append('')
        rows.append(dict(zip(COLUMNS, cells[:len(COLUMNS)])))
    return rows


def to_csv(rows, output='inscriptions.csv'):
    with open(output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ CSV: {output} ({len(rows)} εγγραφές)")


def to_json(rows, output='inscriptions.json'):
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON: {output} ({len(rows)} εγγραφές)")


def to_sqlite(rows, output='inscriptions.db'):
    if os.path.exists(output):
        os.remove(output)
    conn = sqlite3.connect(output)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE inscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {', '.join(f'{col} TEXT' for col in COLUMNS)}
        )
    """)
    for row in rows:
        cur.execute(
            f"INSERT INTO inscriptions ({', '.join(COLUMNS)}) VALUES ({', '.join(['?']*len(COLUMNS))})",
            [row.get(col, '') for col in COLUMNS]
        )
    conn.commit()
    conn.close()
    print(f"✓ SQLite: {output} ({len(rows)} εγγραφές)")
    print(f"  Παράδειγμα queries:")
    print(f"    sqlite3 {output} \"SELECT name, ascii_transcription FROM inscriptions WHERE site='Haghia Triada' LIMIT 5\"")
    print(f"    sqlite3 {output} \"SELECT site, COUNT(*) FROM inscriptions GROUP BY site ORDER BY COUNT(*) DESC\"")


def print_stats(rows):
    print("\n" + "="*50)
    print("ΣΤΑΤΙΣΤΙΚΑ")
    print("="*50)
    print(f"\nΣυνολικές εγγραφές: {len(rows)}")

    sites = Counter(r['site'] for r in rows if r['site'] and r['site'] != 'Unavailable')
    print(f"\nΕγγραφές ανά Site (top 10):")
    for site, count in sites.most_common(10):
        print(f"  {site:<30} {count}")

    supports = Counter(r['support'] for r in rows if r['support'])
    print(f"\nΕγγραφές ανά τύπο αντικειμένου:")
    for support, count in supports.most_common():
        print(f"  {support:<30} {count}")

    periods = Counter()
    for r in rows:
        date = r['date']
        if 'Late Minoan IB' in date:        periods['LM IB (1500-1450 BCE)'] += 1
        elif 'Late Minoan IA' in date:      periods['LM IA (1600-1500 BCE)'] += 1
        elif 'Late Minoan I' in date:       periods['LM I (1600-1450 BCE)'] += 1
        elif 'Middle Minoan' in date:       periods['MM'] += 1
        elif not date or 'Unavailable' in date: periods['Άγνωστη'] += 1
        else:                               periods[date[:30]] += 1
    print(f"\nΕγγραφές ανά περίοδο:")
    for period, count in sorted(periods.items(), key=lambda x: -x[1]):
        print(f"  {period:<35} {count}")

    with_comment = sum(1 for r in rows if r['commentary'])
    print(f"\nΜε commentary:    {with_comment}")
    print(f"Χωρίς commentary: {len(rows) - with_comment}")

    all_syllables = []
    for r in rows:
        if r['ascii_transcription']:
            syllables = re.findall(r'[A-Z][A-Z0-9₂₃₄]*(?:\([^)]+\))?', r['ascii_transcription'])
            all_syllables.extend(syllables)
    print(f"\nΣυχνότερα συλλαβογράμματα (top 15):")
    for syl, count in Counter(all_syllables).most_common(15):
        print(f"  {syl:<10} {count}")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='inscriptions_table.md')
    parser.add_argument('--format', default='all',
                        choices=['all', 'csv', 'json', 'sqlite', 'stats'])
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ΣΦΑΛΜΑ: Δεν βρέθηκε '{args.input}'")
        raise SystemExit(1)

    rows = load_markdown(args.input)
    print(f"Φορτώθηκαν {len(rows)} εγγραφές από '{args.input}'")

    if args.format in ('all', 'csv'):    to_csv(rows)
    if args.format in ('all', 'json'):   to_json(rows)
    if args.format in ('all', 'sqlite'): to_sqlite(rows)
    if args.format in ('all', 'stats'):  print_stats(rows)


if __name__ == '__main__':
    main()
