#!/usr/bin/env python3
"""
build.py - Generates static HTML pages for all Linear A inscriptions.
Παράγει τον φάκελο items/ με ένα .html για κάθε επιγραφή,
και ξαναγράφει το items_image_map.js.

Χρήση:
    python build.py

Απαιτούμενα αρχεία στον ίδιο φάκελο:
    syllables.txt, numbers.txt, inscriptions.json,
    supplement.json, imagemaps.json, template.html
    ../commentary/  (φάκελος με σχόλια)
    items/          (δημιουργείται αυτόματα αν δεν υπάρχει)
"""

import json
import os
from collections import defaultdict

# ── Έλεγχος αρχείων ─────────────────────────────────────────────────────────
required = ['syllables.txt', 'numbers.txt', 'inscriptions.json',
            'supplement.json', 'template.html']
missing = [f for f in required if not os.path.exists(f)]
if missing:
    print("ΣΦΑΛΜΑ: Λείπουν τα παρακάτω αρχεία:")
    for f in missing:
        print(f"  - {f}")
    exit(1)

os.makedirs('items', exist_ok=True)

# ── Φόρτωση transliterations ─────────────────────────────────────────────────
transliterations = {}
for s in open('syllables.txt').readlines():
    sign, value = s.split('\t')
    transliterations[sign] = value.strip()

for s in open('numbers.txt').readlines():
    sign, value = s.split('\t')
    transliterations[sign] = value.strip()

lineara_signs = {v: k for k, v in transliterations.items()}
lineara_signs["*"] = "*"

# ── Φόρτωση δεδομένων ────────────────────────────────────────────────────────
inscriptions = json.load(open('inscriptions.json'))

supplement = json.load(open('supplement.json'))
catalog = {}
dimensions = {}
tabulations = {}
for s in supplement:
    catalog[s["name"]] = s["catalogue"]
    if s["dimensions"]:
        dimensions[s["name"]] = s["dimensions"]
    tabulations[s["name"]] = s["tabulation"]

commentaries = defaultdict(str)
if os.path.isdir("../commentary/"):
    for f in os.scandir("../commentary/"):
        if not f.is_file():
            continue
        content = open(f.path).read()
        nm = f.name.split('.')[0]
        commentaries[nm] = content
        for suff in 'abcdefg':
            commentaries[nm + suff] = content

# ── Χρονολογικά contexts ─────────────────────────────────────────────────────
contexts = {a: b for a, b in [
    ["EM",      "Pre-palace period <br> 3500-1900 BCE"],
    ["EMI",     "Early Minoan I <br> 3500-2900 BCE"],
    ["EMII",    "Early Minoan IIA, IIB <br> 2900-2300 BCE"],
    ["EMIIIi",  "Early Minoan III, Middle Minoan IA <br> 2300-1900 BCE"],
    ["MHIII",   "Middle Helladic <br> 2000-1550 BCE"],
    ["MM",      "Old Palace period <br>  1900-1650 BCE"],
    ["MMI",     "Middle Minoan I  <br>  1900-1800 BCE"],
    ["MMIA",    "Middle Minoan IA  <br>  1900-1850 BCE"],
    ["MMIB",    "Middle Minoan IB  <br>  1900-1800 BCE"],
    ["MMII",    "Middle Minoan II  <br>  1800-1650 BCE"],
    ["MMIIA",   "Middle Minoan IIA  <br>  1800-1750 BCE"],
    ["MMIIB",   "Middle Minoan IIB, IIIA <br>  1750-1650 BCE"],
    ["MMIII",   "Middle Minoan III <br>  1750-1600 BCE"],
    ["MMIIIA",  "Middle Minoan IIB, IIIA  <br> 1750-1650 BCE"],
    ["NP",      "New Palace period  <br> 1650-1450 BCE"],
    ["MMIIIB",  "(first) Middle Minoan IIIB  <br>  1650-1600 BCE"],
    ["LMI",     "Late Minoan I <br>  1600-1450 BCE"],
    ["LMIA",    "Late Minoan IA <br>  1600-1500 BCE"],
    ["LMIB",    "Late Minoan IB  <br>  1500-1450 BCE"],
    ["CM",      "Creto-Mycenaean period  <br>  1450-1100 BCE"],
    ["LHI",     "1550-1450 BCE"],
    ["LBI",     "1550-1400 BCE"],
    ["LMII",    "Third Palace period, Late Minoan II, IIIA1  <br>  1450-1350 BCE"],
    ["LMIII",   "Post Palace period. Late Minoan IIIA2, IIIB, IIIC <br>  1400-1100 BCE"],
    ["LMIIIA",  "Post Palace period. Late Minoan IIIB  <br> 1350-1100 BCE"],
    ["SM",      "Sub-Minoan period  <br> 1100-1000 BCE"],
    ["Geometric", "1000BCE"],
    ["",        "Unavailable"],
]}

# ── Helper functions ──────────────────────────────────────────────────────────
def splitName(name):
    if len(name) < 4:
        return f"{name[:2]} {name[2:]}"
    if name[3] in "abcdfg":
        return f"{name[:2]} {name[2:4]} {name[4:]}"
    if name[3].isnumeric():
        return f"{name[:2]} {name[2:]}"
    if name.startswith("ARKH"):
        return f"{name[:4]} {name[4:]}"
    if len(name) < 5:
        return f"{name[:2]} {name[2:]}"
    if name[4] in "abcdfg":
        return f"{name[:3]} {name[3:5]} {name[5:]}"
    if name[:3] in ["VRY", "THE", "ARM", "PYR"]:
        return f"{name[:3]} {name[3:]}"
    return name

split_names = {s[0]: splitName(s[0]) for s in inscriptions}

def get_image_elements(filenames, url):
    elements = ""
    for f in filenames:
        elements += f'<a href="../{url}" target="_blank"><img src="../{f}" width="300"></a>\n        '
    return elements

def getSiteImage(detail):
    if detail["images"]:
        return f"https://lineara.xyz/{detail['images'][0]}"
    if detail["facsimileImages"]:
        return f"https://lineara.xyz/{detail['facsimileImages'][0]}"
    return "https://lineara.xyz/assets/archer.png"

def createReadingSpec(name, tabulation, parsedInscription):
    run = ""
    line = 1
    spec = []
    for r, row in enumerate(tabulation):
        for sign, status, word_index in row:
            if sign not in transliterations:
                print(f"  [warn] {name}: άγνωστο σημείο '{sign}'")
                s = "*"
            else:
                s = transliterations[sign]
            spec.append(f"{r+1} {line} {word_index} {s} {status if status else 'none'}")
            run += sign
            if parsedInscription.startswith(run + '\n'):
                run += '\n'
                line += 1
    return spec

def createTranscribedAsciiFromSpec(spec):
    output = '       <line><word number="0">'
    pr = pw = None
    for s in spec:
        r, l, w, syl, status = s.split()
        if not pr:
            pr, pw = r, w
        if w != pw:
            output += "</word>"
        if r != pr:
            pr = r
            output += '</line>\n       <line>'
            if w == pw:
                output += f'<word number="{w}">'
        if w != pw:
            pw = w
            output += f'<word number="{w}">'
        if syl.isnumeric() and syl.isascii():
            output += f"<number>{syl}</number>"
        else:
            output += f"<ideogram>{syl}</ideogram>"
    output += "</word></line>"
    return output

def createParsedAsciiFromSpec(spec):
    output = '       <line><word number="0">'
    pl = pw = None
    for s in spec:
        r, l, w, syl, status = s.split()
        if not pl:
            pl, pw = l, w
        if w != pw:
            output += "</word>"
        if l != pl:
            pl = l
            output += '</line>\n       <line>'
        if w != pw:
            pw = w
            output += f'<word number="{w}">'
        if syl.isnumeric() and syl.isascii():
            output += f"<number>{syl}</number>"
        else:
            output += f"<ideogram>{syl}</ideogram>"
    output += "</word></line>"
    return output

# ── Κύριος βρόχος: παραγωγή HTML ─────────────────────────────────────────────
template_base = open("template.html").read()
specs = {}
count = 0

print(f"Παράγω HTML για {len(inscriptions)} επιγραφές...")

for inscription in inscriptions:
    name = inscription[0]
    detail = inscription[1]
    template = template_base

    template = template.replace("%NAME%", name)
    template = template.replace("%NAMES%", ', '.join(detail["names"] + [split_names[name]]))
    template = template.replace("%CONTEXT%", contexts.get(detail["context"], "Unavailable"))
    template = template.replace("%SITE%", detail["site"])
    template = template.replace("%SUPPORT%", detail["support"])
    template = template.replace("%FINDSPOT%", detail["findspot"] or "Unavailable")
    template = template.replace("%SCRIBE%", detail["scribe"] or "Unavailable")
    template = template.replace("%SITE_IMAGE%", getSiteImage(detail))
    template = template.replace("%PHOTO_IMAGES%", get_image_elements(detail["images"], detail["imageRightsURL"]))
    template = template.replace("%PHOTO_SOURCE%", detail["imageRights"])
    template = template.replace("%DRAWING_IMAGES%", get_image_elements(detail["facsimileImages"], detail["imageRightsURL"]))
    template = template.replace("%DRAWING_SOURCE%", detail["imageRights"])
    template = template.replace("%REFERENCES%", f'<a href="../{detail["imageRightsURL"]}">{detail["imageRightsURL"]}</a>')
    template = template.replace("%YOUNGER%", commentaries[name])
    template = template.replace("%CATALOG%", catalog[name] if name in catalog and catalog[name] else "")
    template = template.replace("%MUSEUM%", "Hiraklion Museum" if name in catalog and catalog[name] else "")

    if name in dimensions:
        d = dimensions[name]
        template = template.replace("%HEIGHT%",    d["height"])
        template = template.replace("%LENGTH%",    d["length"])
        template = template.replace("%THICKNESS%", d["thickness"])
        template = template.replace("%SOURCE%",    d["source"])
        template = template.replace("%UNIT%",      d["unit"])
    else:
        for ph in ["%HEIGHT%", "%LENGTH%", "%THICKNESS%", "%SOURCE%", "%UNIT%"]:
            template = template.replace(ph, "")

    if name in tabulations:
        tabulation = tabulations[name]
        parsedInscription = detail["parsedInscription"]
        parsedInscription = parsedInscription.strip("𐝫\n").replace("𐝫", "")

        spec = createReadingSpec(name, tabulation, parsedInscription)
        specs[name] = [s.strip() for s in spec]

        template = template.replace("%SPEC%", '\n'.join(spec))
        template = template.replace("%TRANSCRIBED_ASCII%", createTranscribedAsciiFromSpec(spec))
        template = template.replace("%PARSED_ASCII%",      createParsedAsciiFromSpec(spec))

        laspec = [' '.join(s.split()[:3] + [lineara_signs.get(s.split()[3], '*')] + [s.split()[4]])
                  for s in spec]
        template = template.replace("%TRANSCRIBED_UNICODE%", createTranscribedAsciiFromSpec(laspec))
        template = template.replace("%PARSED_UNICODE%",      createParsedAsciiFromSpec(laspec))
    else:
        print(f"  [warn] {name}: δεν βρέθηκε tabulation")

    with open(f"items/{name}.html", 'w', encoding='utf-8') as out:
        out.write(template)
    count += 1

print(f"✓ {count} HTML αρχεία γράφτηκαν στο items/")

# ── Image map (προαιρετικό - χρειάζεται imagemaps.json) ──────────────────────
if not os.path.exists('imagemaps.json'):
    print("⚠ imagemaps.json δεν βρέθηκε, παράλειψη image map.")
    print("\nΌλα έτοιμα!")
    exit(0)

raw_image_maps = json.load(open('imagemaps.json'))
image_map = {}
for img in raw_image_maps:
    k = img["img"].split('/')[1].split('.')[0]
    image_map[k] = img["areas"]

new_image_map = {}
for inscription, spec in specs.items():
    for img_type in [inscription + "-Inscription", inscription + "-Facsimile"]:
        if img_type not in image_map:
            continue
        coords = [x["coords"] for x in image_map[img_type]]
        if not coords:
            continue
        new_coords = []
        offset = 0
        for i, s in enumerate(spec):
            _, _, word_index, syl, _ = s.split()
            if syl == "*900":
                offset += 1
                new_coords.append({"word": word_index, "ideogram": syl, "coords": {}})
                continue
            idx = i - offset
            new_coords.append({
                "word": word_index,
                "ideogram": syl,
                "coords": coords[idx] if idx < len(coords) else {}
            })
        new_image_map[img_type] = new_coords

with open('items_image_map.js', 'w', encoding='utf-8') as f:
    f.write("const coordinates = \n")
    f.write(json.dumps(new_image_map, ensure_ascii=False, indent=4))

print("✓ items_image_map.js ενημερώθηκε")
print("\nΌλα έτοιμα!")
