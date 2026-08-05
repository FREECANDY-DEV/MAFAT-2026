import urllib.request
import urllib.error
try:
    response = urllib.request.urlopen('https://d4ysu55xg7wfi.cloudfront.net/docs.html')
    print(response.read().decode())
except urllib.error.HTTPError as e:
    print(e.read().decode())
