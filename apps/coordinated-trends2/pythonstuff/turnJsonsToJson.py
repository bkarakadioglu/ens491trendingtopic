import fileinput
#Here is the order: turnJsonsToJson, removeCreatedAt, mergeJsonFiles, takeNameDateVolume, sortDateAndVolume, sessionCreator
filenames = ["Eskişehir_2022-07.jsons","Eskişehir_2022-08.jsons","Eskişehir_2022-09.jsons",
             "Eskişehir_2022-10.jsons","Eskişehir_2022-11.jsons","Eskişehir_2022-12.jsons"]
for filename in filenames:
    for line in fileinput.input(filename, inplace=True):
        if 1 != fileinput.filelineno():
            print(',{}'.format(line), end='')
        else:
            print('[{}'.format(line), end='')
    open(filename,"a").write(']')
     
