import urllib.request, re

req = urllib.request.Request("https://clausler.com/", headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode("utf-8")

matches = re.findall(r'"([^"]*(?:\.js|\.json)[^"]*)"', html)
print("Matched files in HTML:", matches)

# Check buildId
build_id = re.findall(r'buildId:"([^"]+)"', html)
print("Build ID:", build_id)
if build_id:
    manifest_url = f"https://clausler.com/_nuxt/builds/meta/{build_id[0]}.json"
    print("Testing meta url:", manifest_url)
    try:
        data = urllib.request.urlopen(urllib.request.Request(manifest_url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
        print("Meta JSON:", data[:500])
    except Exception as e:
        print("Meta error:", e)

    manifest_url2 = f"https://clausler.com/_nuxt/builds/id/{build_id[0]}.json"
    try:
        data = urllib.request.urlopen(urllib.request.Request(manifest_url2, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
        print("Build id JSON:", data[:500])
    except Exception as e:
        print("Build id error:", e)
