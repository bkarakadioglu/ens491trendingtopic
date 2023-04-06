import json

# load the JSON file into a Python variable
cumhurdata = []
milletdata = []
with open('apps\coordinated-trends\pythonstuff\ewcumhur.json', 'r') as f:
    cumhurdata = json.load(f)

with open('apps\coordinated-trends\pythonstuff\ewmillet.json', 'r') as f:
    milletdata = json.load(f)

data = milletdata + cumhurdata
# save the modified JSON object back to the file
with open('apps\coordinated-trends\pythonstuff\itfkData.json', 'w') as f:
    json.dump(data, f)