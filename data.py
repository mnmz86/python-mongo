import json
data = None
with open("location_data_min.json") as l:
    data = json.loads(l.read())

print(data)