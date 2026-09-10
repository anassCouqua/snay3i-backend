#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from hourly_catalog import build

DARJA_CITIES = ["كازا", "الرباط", "مراكش"]
FRENCH_CITIES = ["Casablanca", "Rabat", "Marrakech"]
DARJA_VARIANTS = [
    ("إلا كنت ف{city}، خليك واضح من الأول. ", "ف{city}"),
    ("ف{city}، قبل ما تختار أي حرفي، قارن المعلومات مزيان. ", "نصيحة ديال {city}"),
    ("هاد النصيحة نافعة خصوصا إلا كنت ف{city}. ", "ف{city} اليوم"),
]
FRENCH_VARIANTS = [
    ("À {city}, commencez par comparer les informations disponibles. ", "À {city}"),
    ("Si vous êtes à {city}, vérifiez les détails avant de choisir. ", "Conseil {city}"),
    ("À {city}, quelques vérifications simples peuvent vous faire gagner du temps. ", "À {city} aujourd'hui"),
]


def make_distinct(slot: int):
    item = build(slot)
    cycle = slot // 8
    script = item["script"]
    meta = item["meta"]
    if script["language"] == "darija":
        city = DARJA_CITIES[cycle % len(DARJA_CITIES)]
        prefix, eyebrow = DARJA_VARIANTS[cycle % len(DARJA_VARIANTS)]
    else:
        city = FRENCH_CITIES[cycle % len(FRENCH_CITIES)]
        prefix, eyebrow = FRENCH_VARIANTS[cycle % len(FRENCH_VARIANTS)]
    script["voice_text"] = prefix.format(city=city) + script["voice_text"]
    script["scenes"][0]["eyebrow"] = eyebrow.format(city=city)
    meta["title"] = f"{meta['title']} · {city}"
    meta["city_rotation"] = city
    meta["variant_cycle"] = cycle
    return item

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--slot", type=int, required=True)
    p.add_argument("--script", required=True)
    p.add_argument("--meta", required=True)
    args = p.parse_args()
    item = make_distinct(args.slot % 24)
    Path(args.script).parent.mkdir(parents=True, exist_ok=True)
    Path(args.script).write_text(json.dumps(item["script"], ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.meta).write_text(json.dumps(item["meta"], ensure_ascii=False, indent=2), encoding="utf-8")
