import requests
from character_creation.models import *
def extract_indexes(response):
    response = response.json()
    indexes = []
    for r in response["results"]:
        indexes.append(r["index"])
    return indexes

def get_unique_instances_of_field(base_url, indexes, field):
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    field_instances = []
    count = 0
    num_indexes = len(indexes)

    for index in indexes:
        url = base_url + "/" + index
        response = requests.request("GET", url, headers=headers, data=payload).json()

        count += 1

        print(f"{count} / {num_indexes} retrieved")

        if response[field] not in field_instances:
            field_instances.append(response[field])

    return field_instances

url = "https://www.dnd5eapi.co/api/equipment-categories"

payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

indexes = extract_indexes(response)
for i in indexes:
    print(i)

# types = get_unique_instances_of_field(url, indexes, "type")
#
# print(types)