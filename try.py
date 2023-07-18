import requests

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
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT6HrGh7EOzzejrvzkG_TGUM_GoGVDuvlUq7UcYqHlESZX6Vv8Hvwatsp4FLdE4Nmff9z5LSG3KQFq9/pub?gid=700061257&single=true&output=csv"
data = make_get_request(url)
li=[]
if data:
    # print(data)
    li.append(data)

print(li[0])