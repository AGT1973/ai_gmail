import urllib.request
import json
import ssl

url = "https://bigthinkmedia.substack.com/api/v1/free"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://bigthinkmedia.substack.com",
    "Referer": "https://bigthinkmedia.substack.com/subscribe"
}

payload = json.dumps({"email": "ai.mpat.designer@gmail.com"}).encode("utf-8")
context = ssl.create_default_context()

try:
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, context=context) as response:
        res = response.read().decode("utf-8")
        print("SUCCESS:", res)
except Exception as e:
    print("RESPONSE:", e)
