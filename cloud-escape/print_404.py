import urllib.request
import urllib.error
try:
    urllib.request.urlopen('https://d4ysu55xg7wfi.cloudfront.net/nonexistent.html')
except urllib.error.HTTPError as e:
    print(e.read().decode())
