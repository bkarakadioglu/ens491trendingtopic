import json
filenamesTurkey = ["Turkey_2022-07.json","Turkey_2022-08.json","Turkey_2022-09.json",
             "Turkey_2022-10.json","Turkey_2022-11.json","Turkey_2022-12.json"]
filenames = ["Eskişehir_2022-07.json","Eskişehir_2022-08.json","Eskişehir_2022-09.json",
             "Eskişehir_2022-10.json","Eskişehir_2022-11.json","Eskişehir_2022-12.json"]
for filename in filenames:
    with open(filename, "r+") as jsonFile:
        data = json.load(jsonFile)
        for element in data:
            del element["created_at"]
        jsonFile.seek(0)
        json.dump(data, jsonFile)
        jsonFile.truncate()