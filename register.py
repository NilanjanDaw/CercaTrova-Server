import getpass
import requests
from cerca_trova.Encryption import encrypt
url = "http://127.0.0.1:8000/personnel_login_server/user/"

def takeInput():
    headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    }

    personnel_id = raw_input("Enter ID: ")
    adhaar_number = raw_input("Enter Adhaar number: ")
    first_name = raw_input("Enter first name: ")
    last_name = raw_input("Enter last name: ")
    contact_number = raw_input("Enter contact number: ")
    car_number = raw_input("Enter vehicle number: ")
    responder_type = raw_input("Enter Emergency responder type: ")
    base_station = raw_input("Enter base station: ")
    password = getpass.getpass('Enter Password: ')
    password = encrypt(password)
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"personnel_id\"\r\n\r\n" + personnel_id + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"adhaar_number\"\r\n\r\n" + str(adhaar_number) + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"first_name\"\r\n\r\n" + first_name + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"last_name\"\r\n\r\n " + last_name + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"contact_number\"\r\n\r\n" + contact_number +"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"car_number\"\r\n\r\n" + car_number + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"responder_type\"\r\n\r\n" + responder_type + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"base_station\"\r\n\r\n" + base_station + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n" + password + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    return payload, headers
    
payload, headers = takeInput()
print "Registering Personnel...",
try:
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 201:
        print "DONE"
    else:
        print "FAILED"
        print(response.text)
except Exception as e:
    print "FAILED"
    print e
