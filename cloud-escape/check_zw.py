import urllib.request
import re

def check_url(url):
    try:
        content = urllib.request.urlopen(url).read().decode('utf-8')
        zw = re.findall(r'[\u200b\u200c\u200d\uFEFF]', content)
        print(f"Zero width characters in {url}: {len(zw)}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

check_url("https://d4ysu55xg7wfi.cloudfront.net/index.html")
check_url("https://d4ysu55xg7wfi.cloudfront.net/docs.html")
