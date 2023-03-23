import fileinput
filenames = ["Turkey_2022-08.jsons","Turkey_2022-09.jsons",
             "Turkey_2022-10.jsons","Turkey_2022-11.jsons","Turkey_2022-12.jsons"]
for filename in filenames:
    for line in fileinput.input(filename, inplace=True):
        if 1 != fileinput.filelineno():
            print(',{}'.format(line), end='')
        else:
            print('[{}'.format(line), end='')
    open(filename,"a").write(']')
     
