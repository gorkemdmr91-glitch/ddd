import json
TRIM_START, TRIM_END = 3.10, 97.50

# (zaman, eski, yeni) — yeni birden fazla kelimeye bölünebilir
DUZELTME = [
    (5.55,  "3",       "üç"),
    (7.53,  "gizem",   "Gizem"),
    (8.63,  "görkem",  "Görkem"),
    (59.41, "görkem",  "Görkem"),
    (93.35, "Erdoğan", "Her zaman"),
]

segs = json.load(open("transkript.json", encoding="utf-8"))
words = [dict(w) for s in segs for w in s["words"] if w["w"].strip()]
words.sort(key=lambda x: x["s"])

for t, old, new in DUZELTME:
    for w in words:
        if abs(w["s"] - t) < 0.06 and w["w"].strip(".,?!").lower() == old.strip(".,?!").lower():
            w["w"] = w["w"].replace(old, new) if old in w["w"] else new
            break

# çok kelimeli düzeltmeleri böl
out = []
for w in words:
    parts = w["w"].split()
    if len(parts) > 1:
        d = (w["e"] - w["s"]) / len(parts)
        for i, p in enumerate(parts):
            out.append({"w": p, "s": round(w["s"] + i * d, 3),
                        "e": round(w["s"] + (i + 1) * d, 3), "p": w["p"]})
    else:
        out.append(w)

# "300" + "-350" gibi bölünmüş tokenleri birleştir
merged = []
for w in out:
    if merged and w["w"].startswith("-") and len(w["w"]) > 1 \
            and merged[-1]["w"][-1:].isdigit():
        merged[-1]["w"] += w["w"]
        merged[-1]["e"] = w["e"]
    else:
        merged.append(w)
out = merged

kept = []
for w in out:
    if w["s"] >= TRIM_START - 0.01 and w["s"] < TRIM_END:
        kept.append({"w": w["w"],
                     "s": round(max(0.0, w["s"] - TRIM_START), 3),
                     "e": round(min(w["e"], TRIM_END) - TRIM_START, 3),
                     "p": w["p"]})

json.dump([{"start": 0, "end": TRIM_END - TRIM_START, "text": "", "words": kept}],
          open("transkript_fix.json", "w"), ensure_ascii=False, indent=1)
print(f"kesim: {TRIM_START}-{TRIM_END}s ({TRIM_END-TRIM_START:.2f}s)")
print(f"kelime: {len(out)} -> {len(kept)}")
print("ilk:", kept[0]["w"], kept[0]["s"], "| son:", kept[-1]["w"], kept[-1]["e"])
