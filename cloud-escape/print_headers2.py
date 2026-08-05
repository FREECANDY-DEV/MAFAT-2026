import urllib.request
try:
    response = urllib.request.urlopen('https://d4ysu55xg7wfi.cloudfront.net/test.html')
    print("SUCCESS headers:", response.headers)
except Exception as e:
    if hasattr(e, 'headers'):
        print("ERROR headers:", e.headers)
    else:
        print("ERROR:", e)
