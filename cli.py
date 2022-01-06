import requests 
import time

while True:
    response = requests.get("http://127.0.0.1:5000/ping", headers={"x-secret-key":"2286872938"})
    print(response.text)
    while "pong" in response.text:
        response = requests.get("http://127.0.0.1:5000/ping", headers={"x-secret-key":"2286872938"})
        print(response.text)
    else:
        value = response.headers['Retry-After']
        value = float(value)
        time.sleep(value)