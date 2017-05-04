import requests
import threading
import time

url = "http://127.0.0.1:8000/emergency/notify/"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"user_adhaar_number\"\r\n\r\n123456789011\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"emergency_type\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"location\"\r\n\r\nPOINT( 22.574746 88.433815)\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    }
def test(name="thread"):
    response = requests.request("POST", url, data=payload, headers=headers)
    print"\n%s %s" % (response.status_code, time.ctime(time.time()))

try:
    threads = []
    for i in range(50):
        t = threading.Thread(target=test)
        threads.append(t)
    for i in range(50):
        threads[i].start()
except Exception as e:
   print e
