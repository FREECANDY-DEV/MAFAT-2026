import urllib.request
req = urllib.request.Request('https://userd8a2f72fe43094e8.s3.amazonaws.com/', method='HEAD')
try:
    urllib.request.urlopen(req)
except Exception as e:
    print(e.headers.get('x-amz-bucket-region', 'Not Found'))
