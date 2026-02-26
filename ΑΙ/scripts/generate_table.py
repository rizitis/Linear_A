#!/usr/bin/env python3
"""
generate_table.py - Διαβάζει όλα τα HTML αρχεία από τον φάκελο items/
και παράγει έναν πίνακα Markdown με όλες τις πληροφορίες.

Χρήση:
    python generate_table.py
    python generate_table.py --items-dir /path/to/items
    python generate_table.py --output mytable.md
"""

import os
import re
import argparse


def extract_tag(content, tag):
    match = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', content, re.DOTALL | re.IGNORECASE)
    if match:
        text = re.sub(r'<[^>]+>', ' ', match.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return ''


def extract_reading(content, reading_tag):
    block = re.search(rf'<{reading_tag}.*?>(.*?)</{reading_tag}>', content, re.DOTALL | re.IGNORECASE)
    if not block:
        return ''
    reading_text = re.search(r'<reading-text>(.*?)</reading-text>', block.group(1), re.DOTALL | re.IGNORECASE)
    if not reading_text:
        return ''
    lines_raw = re.findall(r'<line>(.*?)</line>', reading_text.group(1), re.DOTALL)
    lines = []
    for line in lines_raw:
        tokens = re.findall(r'<(?:ideogram|number)>(.*?)</(?:ideogram|number)>', line, re.DOTALL)
        if tokens:
            lines.append(' '.join(tokens))
    return ' / '.join(lines)


def extract_commentary(content):
    match = re.search(r'<commentary-entry>(.*?)</commentary-entry>', content, re.DOTALL | re.IGNORECASE)
    if not match:
        return ''
    text = match.group(1)
    text = re.sub(r'<a href=.*?</a>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 400:
        text = text[:400] + '...'
    return text


def extract_reference(content):
    match = re.search(r'<bibliography-entry>\s*<a href="([^"]+)"', content, re.IGNORECASE)
    if match:
        return match.group(1).replace('../', '')
    return ''


def process_file(filepath):
    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        return {
            'name':                  extract_tag(content, 'name'),
            'support':               extract_tag(content, 'support'),
            'site':                  extract_tag(content, 'site'),
            'findspot':              extract_tag(content, 'findspot'),
            'scribe':                extract_tag(content, 'scribe'),
            'date':                  extract_tag(content, 'context'),
            'ascii_transcription':   extract_reading(content, 'transcribed-reading-ascii'),
            'unicode_transcription': extract_reading(content, 'transcribed-reading-unicode'),
            'reference':             extract_reference(content),
            'commentary':            extract_commentary(content),
        }
    except Exception as e:
        print(f"  [warn] {os.path.basename(filepath)}: {e}")
        return None


def escape_md(text):
    if not text:
        return ''
    text = text.replace('\n', ' ').replace('\r', '')
    # Αφαίρεσε τυχόν ήδη escaped pipes
    text = re.sub(r'\\+\|', '|', text)
    # Full-width pipe για να μη σπάει ο πίνακας
    text = text.replace('|', '｜')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--items-dir', default='items')
    parser.add_argument('--output', default='inscriptions_table.md')
    args = parser.parse_args()

    if not os.path.isdir(args.items_dir):
        print(f"ΣΦΑΛΜΑ: Δεν βρέθηκε φάκελος '{args.items_dir}'")
        raise SystemExit(1)

    html_files = sorted([f for f in os.listdir(args.items_dir) if f.endswith('.html')])

    if not html_files:
        print(f"ΣΦΑΛΜΑ: Δεν βρέθηκαν HTML αρχεία στο '{args.items_dir}'")
        raise SystemExit(1)

    print(f"Βρέθηκαν {len(html_files)} αρχεία στο '{args.items_dir}'...")

    rows = []
    for filename in html_files:
        data = process_file(os.path.join(args.items_dir, filename))
        if data:
            rows.append(data)

    headers = ['Name', 'Support', 'Site', 'Findspot', 'Scribe', 'Date',
               'Transcription (ASCII)', 'Transcription (Linear A)', 'Reference', 'Commentary']
    keys = ['name', 'support', 'site', 'findspot', 'scribe', 'date',
            'ascii_transcription', 'unicode_transcription', 'reference', 'commentary']

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('# Linear A Inscriptions\n\n')
        f.write('| ' + ' | '.join(headers) + ' |\n')
        f.write('|' + '|'.join(['---'] * len(headers)) + '|\n')
        for row in rows:
            cells = [escape_md(row.get(k, '')) for k in keys]
            f.write('| ' + ' | '.join(cells) + ' |\n')

    print(f"✓ {len(rows)} εγγραφές γράφτηκαν στο '{args.output}'")


if __name__ == '__main__':
    main()
