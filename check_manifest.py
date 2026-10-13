import urllib.request, json

url = "https://clausler.com/_nuxt/builds/meta/51770737-52f0-443c-aa12-9eda28ebfdc2.json"
data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8'))
print(data)

# Try fetching /_nuxt/builds/latest.json
try:
    latest = urllib.request.urlopen(urllib.request.Request("https://clausler.com/_nuxt/builds/latest.json", headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
    print("Latest:", latest)
except Exception as e:
    print("Latest error:", e)

# Try fetching manifest.json
try:
    man = urllib.request.urlopen(urllib.request.Request("https://clausler.com/_nuxt/manifest.json", headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
    print("Manifest:", man[:500])
except Exception as e:
    print("Manifest error:", e)
