import urllib.request, re

url = "https://clausler.com/_nuxt/hMcJH_hd.js"
s = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
print("Bundle size:", len(s))

# Find all plain text snippets in the bundle longer than 20 chars
clean_strings = re.findall(r'[\'"`]([A-Za-z0-9\s.,!?:;\-\–]{20,200})[\'"`]', s)
print(f"Total phrases found: {len(clean_strings)}")
with open(r"C:\Users\roshu\.gemini\antigravity\scratch\redline-local\clausler_phrases.txt", "w", encoding="utf-8") as out:
    for item in clean_strings:
        out.write(item + "\n")
print("Done writing clausler_phrases.txt")
