#!/usr/bin/env python3

import time
import os
import requests
import json
from dotenv import load_dotenv
from base64 import b64encode
from token_manager import get_token, check_token
from datetime import datetime
from pytz import timezone

# Load the access token from token_manager.py
access_token = check_token()

# Get the list of documents
next_url = 'https://cad.onshape.com/api/documents'
all_data = []

# Loop through the pages of documents because pagination is annoying
print(f'Paginating through documents... Please be patient')
while next_url:
    response = requests.get(next_url, headers={'Accept': 'application/vnd.onshape.v1+json', 'Authorization': 'Bearer ' + access_token})
    data = json.loads(response.text)
    all_data.extend(data['items'])
    next_url = data['next']
    #print(next_url)
    # be kind to the API
    time.sleep(1)

# Write the response to a file
with open('response.json', 'w') as outfile:
    json.dump(all_data, outfile)

# Read the response from the file
with open("response.json", "r") as json_file:
    documents = json.load(json_file)

# Find the document that was last modified
most_recent = max(documents, key=lambda x: x['modifiedAt'])

# Print the name of the last person to modify the document
print('Name: ' + most_recent['name'])

# Convert the timestamp to a datetime object
timestamp = datetime.strptime(most_recent['modifiedAt'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
# Set the timezone to UTC
utc_time = timezone('UTC').localize(timestamp)
# Convert the UTC time to your local time
local_time = utc_time.astimezone(timezone('US/Mountain'))
#print('Modified: ' + most_recent['modifiedAt'])

# Get the link to the document
link = most_recent['href']
# strip the api version from the link
link = link.replace("/api/v1", "")
print('Link: ' + link)

# Print the local time
print('Modified:', local_time)

# Write the output to a file
with open("output.txt", "w") as f:
    f.write("Link: " + link+"\n")
