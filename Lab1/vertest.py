

import requests

print requests.__version__

response = requests.get("http://www.google.com/")

print response.status_code

print response.headers['content-type']

print response.encoding

# print response.text

