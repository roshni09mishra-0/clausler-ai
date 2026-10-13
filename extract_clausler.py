import re

fpath = r"C:\Users\roshu\.gemini\antigravity\brain\50aeb490-c3e5-46db-97fe-8752b3bde50b\.system_generated\steps\283\content.md"
with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
    txt = f.read()

terms = ["clause", "contract", "freelance", "risk", "report", "negotiat", "exposure", "upload", "liability"]
matches = []
for s in re.findall(r'"([^"\\]{15,150})"', txt):
    s_low = s.lower()
    if any(t in s_low for t in terms):
        matches.append(s)

unique_matches = list(dict.fromkeys(matches))
print(f"Total found: {len(unique_matches)}")
with open(r"C:\Users\roshu\.gemini\antigravity\scratch\redline-local\scratch_clausler_strings.txt", "w", encoding="utf-8") as out:
    for m in unique_matches[:60]:
        out.write(m + "\n")
print("Saved to scratch_clausler_strings.txt")
