import MyPreConfigs
import NewBinaryManips
import AISData

f = open(MyPreConfigs.AISFileName, "r")
try:
    loop = True
    count = 0
    while count < 100:
        count += 1
        string = f.readline()
        if len(string) == 0:
            loop = False
        # print ( string[0:-2])

        try:
            initialise = MyPreConfigs.MyPreConfigs()
        except Exception as e:
            raise RuntimeError("error initialising PreConfigs")
        """ the __init__ function in MyPreconfigs will read ini file
        and set any variables that are different from the defaults
        """

        diagnostic = MyPreConfigs.diagnostic
        diagnostic2 = MyPreConfigs.diagnostic2
        diagnostic3 = MyPreConfigs.diagnostic3

        try:

            processed = False
        except Exception as e:
            raise RuntimeError("getting file- error", e)

        # now the guts of processing the incoming AIS Data
        # have an  encoded string break it down
        if not processed and (len(string) > 0) and string[0] == "!":
            aisfields = AISData.Dissemble_encoded_string(string)
            if aisfields[1] != "1":
                # print ('Input fragment' , aisfields)
                pass

            # now create an AIS_Data ob ject

            myAIS = AISData.AIS_Data(
                aisfields[0],
                aisfields[1],
                aisfields[2],
                aisfields[3],
                aisfields[4],
                aisfields[5],
                aisfields[6],
            )
            s = format(bin(myAIS.AIS_Binary_Payload))
            s = s[3:]
            while len(s) < len(aisfields[5]) * 6:
                s = "0" + s
            print("AIS_BinaryPayload")
            print(s)

            # now call the new create binary payload
            binarypayload = NewBinaryManips.new_create_binary_payload(aisfields[5])
            s2 = ""
            for x in binarypayload:
                s2 = s2 + format(x, "08b")

            print(s2, "\r\nNew Binary Payload above")

            strpayload = NewBinaryManips.newer_create_binary_payload(aisfields[5])
            print(strpayload)

            # now compare them bit by bit

            if len(s) != len(s2):
                print(
                    "length old binary payload = ",
                    len(s),
                    " length of new binary payload = ",
                    len(s2),
                    "length str_payload = ",
                    len(strpayload),
                )
                print(string[0:-2])
                print(s)
                print(s2)
                print(strpayload)
                for i in range(0, min(len(s), len(s2))):
                    if s[i] != s2[i]:
                        print(" s s1 differ at position ", i)
                    if s[i] != strpayload[i]:
                        print("s and Str_payload differ at posdition ", 1)


except:
    raise RuntimeError()


def main(self):
    pass


if __name__ == 'main':
    main()
