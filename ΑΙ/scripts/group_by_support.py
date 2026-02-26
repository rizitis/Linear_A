#!/usr/bin/env python3
"""
group_by_support.py - Ομαδοποιεί τις επιγραφές ανά τύπο αντικειμένου
και παράγει ένα Markdown αρχείο με ξεχωριστό πίνακα για κάθε κατηγορία.

Χρήση:
    python group_by_support.py
    python group_by_support.py --input inscriptions_table.md
    python group_by_support.py --output grouped_by_support.md
"""

import re
import argparse
import os
from collections import defaultdict

COLUMNS = [
    'name', 'support', 'site', 'findspot', 'scribe', 'date',
    'ascii_transcription', 'unicode_transcription', 'reference', 'commentary'
]

HEADERS = [
    'Name', 'Site', 'Findspot', 'Scribe', 'Date',
    'Transcription (ASCII)', 'Transcription (Linear A)', 'Reference', 'Commentary'
]

# Κλειδιά χωρίς το 'support' (δεν χρειάζεται στον πίνακα, είναι ο τίτλος)
KEYS = [
    'name', 'site', 'findspot', 'scribe', 'date',
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
        cells = [c.strip() for c in line.split('|')]
        if cells and cells[0] == '':
            cells = cells[1:]
        if cells and cells[-1] == '':
            cells = cells[:-1]
        if cells and cells[0] == 'Name':
            continue
        if len(cells) < 6:
            continue
        while len(cells) < len(COLUMNS):
            cells.append('')
        rows.append(dict(zip(COLUMNS, cells[:len(COLUMNS)])))
    return rows


def normalize_support(support):
    """Κανονικοποίηση για συγχώνευση παρόμοιων τύπων (π.χ. Clay vessel / clay vessel)."""
    return support.strip().lower().capitalize() if support else 'Unknown'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='inscriptions_table.md')
    parser.add_argument('--output', default='grouped_by_support.md')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ΣΦΑΛΜΑ: Δεν βρέθηκε '{args.input}'")
        raise SystemExit(1)

    rows = load_markdown(args.input)
    print(f"Φορτώθηκαν {len(rows)} εγγραφές από '{args.input}'")

    # Ομαδοποίηση
    groups = defaultdict(list)
    for row in rows:
        support = normalize_support(row.get('support', ''))
        groups[support].append(row)

    # Ταξινόμηση: πρώτα οι μεγαλύτερες ομάδες
    sorted_groups = sorted(groups.items(), key=lambda x: -len(x[1]))

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('# Linear A Inscriptions — Ομαδοποίηση ανά Τύπο Αντικειμένου\n\n')

        # Πίνακας περιεχομένων
        f.write('## Περιεχόμενα\n\n')
        for support, group_rows in sorted_groups:
            anchor = re.sub(r'[^a-z0-9]+', '-', support.lower()).strip('-')
            f.write(f'- [{support}](#{anchor}) ({len(group_rows)})\n')
        f.write('\n---\n\n')

        # Πίνακας για κάθε κατηγορία
        for support, group_rows in sorted_groups:
            anchor = re.sub(r'[^a-z0-9]+', '-', support.lower()).strip('-')
            f.write(f'## {support}\n\n')
            f.write(f'**{len(group_rows)} εγγραφές**\n\n')

            f.write('| ' + ' | '.join(HEADERS) + ' |\n')
            f.write('|' + '|'.join(['---'] * len(HEADERS)) + '|\n')

            for row in sorted(group_rows, key=lambda x: x.get('name', '')):
                cells = [row.get(k, '') for k in KEYS]
                f.write('| ' + ' | '.join(cells) + ' |\n')

            f.write('\n')

    print(f"✓ {len(sorted_groups)} κατηγορίες γράφτηκαν στο '{args.output}'")
    for support, group_rows in sorted_groups:
        print(f"  {support:<30} {len(group_rows)}")


if __name__ == '__main__':
    main()
