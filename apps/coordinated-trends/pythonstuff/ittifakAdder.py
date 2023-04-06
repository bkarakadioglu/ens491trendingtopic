import json

# load the JSON file into a Python variable
with open('apps\coordinated-trends\pythonstuff\millet181.json', 'r') as f:
    data = json.load(f)

# add a new key-value pair to each item in the JSON object
for item in data:
    item['ittifak'] = 0

# save the modified JSON object back to the file
with open('apps\coordinated-trends\pythonstuff\ewmillet.json', 'w') as f:
    json.dump(data, f)