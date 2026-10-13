import urllib.request, re

chunks = ['./DPJ6qTw1.js', './Dgo2GC_u.js', './BImrRxjO.js', './DlAUqK2U.js', './CNUxFPzM.js', './DU8GM4Dg.js', './Bg_SwxQN.js', './Dnox8c57.js', './CAgjhrDo.js', './CJAZRfQu.js', './BMayDS1c.js', './DeUibkVq.js', './DXn-nAig.js', './CvUfOZlG.js', './_O8rY8ey.js', './C6KuqV4Z.js', './BaL3z7KY.js', './BmY1B1Cn.js', './D-9R2Uhq.js', './CH61QQZN.js', './BjM5ER0X.js', './BSm9JqmE.js', './BjmwIh4Y.js', './CbumGuEP.js', './xBZ_128n.js', './D1hgUAEb.js', './DVqwvcy9.js', './CZKzC0VN.js']

all_phrases = []

for ch in chunks:
    filename = ch.replace('./', '')
    url = f"https://clausler.com/_nuxt/{filename}"
    try:
        content = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
        # Extract meaningful english strings
        matches = re.findall(r'[\'"`]([A-Z][A-Za-z0-9\s.,!?:;\-\–]{15,120})[\'"`]', content)
        if matches:
            all_phrases.append(f"=== {filename} ===")
            all_phrases.extend(matches)
    except Exception as e:
        all_phrases.append(f"Failed {filename}: {e}")

with open(r"C:\Users\roshu\.gemini\antigravity\scratch\redline-local\clausler_chunk_phrases.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(all_phrases))

print(f"Total phrases found: {len(all_phrases)}")
