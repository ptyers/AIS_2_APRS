# extracts all type 24 (and since we grag fragments probanly type 5) records from the arc hived AISdatastream.txt file
# creates anew file Type24data.txt
#
f = open("AISdatastream.txt", "r")

s24 = open("Type24data.txt", "w")
string24 = ""
fields = []
while True:
    string24 = f.readline()
    if len(string24) == 0:
        break
    fields = string24.split(",")

    if fields[5][0] == "H":
        s24.write(string24)
        pass


def main(self):
    pass


if __name__ == 'main':
    main()

