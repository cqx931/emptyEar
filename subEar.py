import httplib, subprocess

c = httplib.HTTPConnection('192.168.204.150', 80)
c.request('POST', '/hello', '{}')
doc = c.getresponse().read()
print doc