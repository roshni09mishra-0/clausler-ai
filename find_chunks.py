import urllib.request, re

req = urllib.request.Request("https://clausler.com/", headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode("utf-8")

scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html)
links = re.findall(r'<link[^>]*href=["\']([^"\']+)["\']', html)
print("Scripts:", scripts)
print("Links:", links)

# Now check the main bundle hMcJH_hd.js for any other chunk imports
for s in scripts:
    url = f"https://clausler.com{s}" if s.startswith('/') else s
    print("Fetching script:", url)
    try:
        s_content = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
        other_chunks = re.findall(r'/[_a-zA-Z0-9/-]+\.[a-zA-Z0-9]+\.js', s_content)
        print("Discovered chunks in", s, ":", set(other_chunks[:10]))
    except Exception as e:
        print("Error fetching script:", e)
