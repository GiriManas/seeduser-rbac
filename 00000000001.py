import requests
print("Testing timeout...")
try:
    requests.post("http://10.255.255.1:5999", timeout=(5,60))
except Exception as e:
    print("Timeout worked:", type(e), e)