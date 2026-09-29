import json, sys
from faster_whisper import WhisperModel

m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segments, info = m.transcribe(
    "ses.wav",
    language="tr",
    word_timestamps=True,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=350),
    beam_size=5,
    condition_on_previous_text=True,
    initial_prompt="Mistanbul Döner, Dönerci Sadık Usta, Volkan Usta, ücretsiz tadım kampanyası, et döner, müşteri memnuniyeti.",
)
out = []
for s in segments:
    out.append({
        "start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(),
        "words": [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3),
                   "p": round(w.probability, 3)} for w in (s.words or [])],
    })
    print(f"[{s.start:7.2f} -> {s.end:7.2f}] {s.text.strip()}", flush=True)
json.dump(out, open("transkript.json", "w"), ensure_ascii=False, indent=1)
print(f"\nDONE segments={len(out)} duration={info.duration:.1f}s lang={info.language} prob={info.language_probability:.2f}")
