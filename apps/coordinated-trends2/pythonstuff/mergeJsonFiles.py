import json
files=["Turkey_2022-07.json","Turkey_2022-08.json","Turkey_2022-09.json",
       "Turkey_2022-10.json","Turkey_2022-11.json","Turkey_2022-12.json"]
filenames = ["Eskişehir_2022-07.json","Eskişehir_2022-08.json","Eskişehir_2022-09.json",
             "Eskişehir_2022-10.json","Eskişehir_2022-11.json","Eskişehir_2022-12.json"]
def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open('Eskisehir_All.json', 'w') as output_file:
        json.dump(result, output_file)

merge_JsonFiles(filenames)