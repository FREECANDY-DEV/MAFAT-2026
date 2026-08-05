import urllib.request
response = urllib.request.urlopen('https://d4ysu55xg7wfi.cloudfront.net/index.html')
print(response.headers)
