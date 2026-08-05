import urllib.request
try:
    response = urllib.request.urlopen('https://d4ysu55xg7wfi.cloudfront.net/test.html')
    print("SUCCESS:", response.read().decode())
except Exception as e:
    if hasattr(e, 'read'):
        print("ERROR BODY:", e.read().decode())
    else:
        print("ERROR:", e)
