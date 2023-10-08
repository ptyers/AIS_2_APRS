f = open("AISdatastream.txt", "r")
out = open("FragmentsStream.txt", "w")


while True:
    try:

        input = f.readline()
        print(input)
        if len(input) > 0:
            fields = input.split(",")
            print(fields)
            if fields[1] != "1":

                out.write(input)

    except Exception as e:
        f.close()
        out.close()
        raise RuntimeError(e)
