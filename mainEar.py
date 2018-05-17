import requests

# To get the ip address of the server: ipconfig getifaddr en1
# Connecting to the server with: nc -v IP 80

url = 'http://192.168.204.150'
query = {'field': "Text Display"}
res = requests.post(url, data=query)
print(res.text)