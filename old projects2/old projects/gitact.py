import urllib.request
from urllib.error import HTTPError, URLError
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("username")
args = parser.parse_args()
username = args.username
url = f"https://api.github.com/users/{username}/events"
try:
    with urllib.request.urlopen(url) as response:
        data = response.read()
        events = json.loads(data)
        n = 0 
        for event in events:
            type_event = event["type"]
            if type_event == "WatchEvent":
                print(username, "starred", event["repo"]["name"])
            elif type_event == "PushEvent":
                print(username, "pushed to", event["repo"]["name"])
            elif type_event == "PublicEvent":  
                print(username, "made a repository public:", event["repo"]["name"])
            elif type_event == "CreateEvent":   
                print(username, "created a", event["payload"]["ref_type"], "in", event["repo"]["name"])
            else:
                print(type_event, "unsupported event")
except HTTPError:
    print("User not found")
except URLError:
    print("Could not connect to GitHub")



    
