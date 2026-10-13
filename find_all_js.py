import urllib.request, re

url = "https://clausler.com/_nuxt/hMcJH_hd.js"
s = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')

# Search for any string ending in .js
js_files = re.findall(r'["\']([a-zA-Z0-9_\-\.\/]+\.js)["\']', s)
print("Referenced .js files in bundle:", set(js_files))
