import urllib.request

docs = urllib.request.urlopen('https://d4ysu55xg7wfi.cloudfront.net/docs.html').read()
index = urllib.request.urlopen('https://d4ysu55xg7wfi.cloudfront.net/index.html').read()

print("docs trailing whitespace:")
for line in docs.split(b'\n'):
    stripped = line.rstrip(b' \t\r')
    trailing = line[len(stripped):]
    if trailing and trailing != b'\r':
        print(repr(trailing))

print("index trailing whitespace:")
for line in index.split(b'\n'):
    stripped = line.rstrip(b' \t\r')
    trailing = line[len(stripped):]
    if trailing and trailing != b'\r':
        print(repr(trailing))
