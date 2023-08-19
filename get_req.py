import requests
import time
from threading import Thread, Lock
def make_get_request(url):
    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.text  # If you expect JSON data, use response.json() instead of response.text
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
url = "http://192.168.4.1"
data = make_get_request(url)

if data:
    print(data)
    li=data.split(",")
    print("Total Time",li[0])
    print("Production Time",li[1])
    print("n-Prod Time",li[2])
    print("Clock Time",li[3])
    print("part count",li[4])
    print("real_time",li[5])
    # print("var1",li[6])
    # print("current ",li[7])