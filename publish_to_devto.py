import os
import sys
import json
import urllib.request
import urllib.error

def publish(api_key, publish_live=True):
    post_file = os.path.join(os.path.dirname(__file__), "DEVTO_POST.md")
    if not os.path.exists(post_file):
        print(f"Error: {post_file} not found")
        sys.exit(1)

    with open(post_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse title from first # heading or frontmatter
    title = "The Freelancer’s Legal Shield: Why I Built an Air-Gapped AI Contract Auditor & Side Hustle"
    
    payload = {
        "article": {
            "title": title,
            "published": publish_live,
            "body_markdown": content,
            "tags": ["hacktoberfest", "opensource", "ai", "webdev"],
            "main_image": "https://raw.githubusercontent.com/roshni09mishra-0/clausler-ai/main/public/cover_image.jpg",
            "canonical_url": "https://clausler-ai.vercel.app"
        }
    }

    req = urllib.request.Request(
        "https://dev.to/api/articles",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "api-key": api_key.strip(),
            "Content-Type": "application/json",
            "User-Agent": "ClauslerPublisher/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("\n[SUCCESS] Article published to DEV.to!")
            print(f"URL: {data.get('url')}")
            return data.get("url")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"\n[HTTP Error] {e.code}: {e.reason}")
        print(f"Details: {error_body}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[Error]: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python publish_to_devto.py <YOUR_DEVTO_API_KEY> [--draft]")
        sys.exit(1)
    api_key = sys.argv[1]
    is_live = "--draft" not in sys.argv
    publish(api_key, publish_live=is_live)
