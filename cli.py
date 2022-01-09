import requests 
import time
import sys 

argument_header = sys.argv[1]

def sending_requests(argument_header):
    while True:
        response = requests.get("http://127.0.0.1:5000/ping", headers={"x-secret-key":argument_header})
        print(response.text)
        time.sleep(1)
        if "error" in response.text:
            value = response.headers['Retry-After']
            value = float(value)
            time.sleep(value)

if __name__ == "__main__":
    sending_requests(argument_header)