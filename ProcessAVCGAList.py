import AVCGAmmsi
import GlobalDefinitions
from configparser import ConfigParser


# used to take in a CSV version of the Portal Spreadsheet AVCGA EPIRB MMSI.xls saved as CSV
# and create a Dictionary keyed on MMSI of AVCGA vessels
#


def ProcessAVCGAList():
    loop = True
    AVCGADict = {}
    filename = (
            GlobalDefinitions.Global.WorkingDir + "\\" + GlobalDefinitions.Global.AVCGAList
    )
    try:
        csv = open(filename, "r")
    except FileNotFoundError:  # file non-existent
        return AVCGADict

    x = 11  # column in csv file containing MMSI (0 based)

    while loop:
        instring = csv.readline()
        if instring != "":
            # reads tpo EOF indicated by a null return
            list = instring.split(",")
            if list[x] != "" and list[x].isnumeric():
                while len(list[x]) < 9:
                    list[x] = "0" + list[x]
                AVCGADict[list[x]] = (
                    list[0],
                    list[1],
                    list[2],
                    list[3],
                    list[4],
                    list[5],
                    list[6],
                    list[7],
                    list[8],
                    list[9],
                    list[10],
                    list[11],
                    list[12],
                    list[13],
                    list[14],
                )
        else:
            loop = False

    csv.close()

    return AVCGADict


def main(self):
    pass


if __name__ == 'main':
    main()
