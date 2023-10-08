import GlobalDefinitions
import MyPreConfigs
from datetime import datetime
import AISData


def handle_fragments(payload):
    # payload id the tuple aisfields
    # returns True when all fragments found and merged
    # during processing will also flush out out dictionary entries older than preset amount

    FragdictTTL = GlobalDefinitions.Global.FragDictTTL

    diagnostic = GlobalDefinitions.Global.diagnostic
    diagnostic2 = GlobalDefinitions.Global.diagnostic2
    diagnostic3 = GlobalDefinitions.Global.diagnostic3

    aisfields = payload
    FragDict = GlobalDefinitions.Global.FragDict
    success = False  # used to determine if we return an AISOject or None
    deleteme = []

    if diagnostic3:
        print(" in handle_fragments payload =\r\n", payload)
        pass

    # if aisfields[5][0] == '5' and aisfields[2] == '1':
    # print(aisfields)

    # structure
    """ Get Fragment"""
    """ Stash it away with time stamp"""
    currenttime = datetime.now()

    # for usage later append currenttime to aisfields
    aisfields.append(currenttime)
    try:
        CurrMessage = int(aisfields[3])
    except ValueError:
        # wasnt an integer representation
        CurrMessage = -1

    # put it in Dictionary
    # since we need to define records of the same message id and also clean up
    # the FragDict to keep it small use a tuple key of MessageNumber/FragmentNumber
    ExtractedFrags = {}
    # print('prior adding FragDicy MessageNo = ', aisfields[3], 'FragmentNo = ', aisfields[2])
    FragDict[aisfields[3], aisfields[2]] = aisfields
    for key in FragDict:
        # print(FragDict[key])
        pass
    """ Check for others """
    """ If YES Create a list of matching message ids"""
    if diagnostic3:
        print("checking for matches")
        pass
    for key in FragDict:  # scan through fragment numbers with common message number
        if diagnostic3:
            print(FragDict[key], aisfields[1])
        try:
            testfrag = FragDict[key]
            if diagnostic3:
                print(" finding matches testfrag ", testfrag)

            if testfrag[3] == aisfields[3]:  # matching message number
                if diagnostic3:
                    print("match found", testfrag)

                ExtractedFrags[testfrag[2]] = testfrag
        except KeyError:
            if diagnostic:
                print("key error in checking")
                # failed because of missing fragment number
        except Exception as e:
            raise RuntimeError(
                "in handle fragments error other than keyerror", e
            ) from e

    """' Have got them all ?"""
    if len(ExtractedFrags) == int(
        aisfields[1]
    ):  # Have we same number of fragments as Fragment Count?
        # YES

        if diagnostic3:
            print("Have complete set of fragments")
            for x in ExtractedFrags:
                print("fragno {} Fragment {} ".format(int(x), ExtractedFrags[x]))

        """ If YES find fragment 1 and create AISObject"""

        try:
            aisfields = ExtractedFrags["1"]
        except KeyError as e:
            raise RuntimeError(
                "No fragment 1 in supposed full set of fragment", e
            ) from e
        if diagnostic3:
            print("creating AIS record myAIS")
        # create an AISObject from Fragment 1
        myAIS = AISData.AIS_Data(
            aisfields[0],
            aisfields[1],
            aisfields[2],
            aisfields[3],
            aisfields[4],
            aisfields[5],
            aisfields[6],
        )

        """ Loop through rest of fragments"""
        """     If necessary remove fill bits from fragment(current-1)"""
        """'    append binary list from current fragment"""
        if diagnostic3:
            print("about to scan records aisdfields[1] = ", int(aisfields[1]))
        x = 2
        while x <= int((aisfields[1])):  # from frag 2 to Fragcount
            testfrag = ExtractedFrags[str(x)]
            lastfrag = ExtractedFrags[str(x - 1)]
            if diagnostic3:
                print("testfrag ", testfrag)
                print(
                    "lastfrag ",
                    lastfrag,
                )
            # check if fill bits were used in previous fragment
            if lastfrag[6][0] != "0":  # fill bits were used
                # remove fill bits from myAIS.AIS_Binary_Payload
                # by slicing the string removing last fill chars bits
                myAIS.AIS_Binary_Payload = myAIS.AIS_Binary_Payload[
                    0 : -(int(lastfrag[6][0]))
                ]
                if diagnostic3:
                    print("Fill bits removed\n", myAIS.AIS_Binary_Payload)
            # just append the binary string created from testfrag to myAIS.AIS_Binary_Payload
            addedbinary, addedlength = AISData.AIS_Data.create_binary_payload(
                testfrag[5]
            )
            if diagnostic3:
                print(addedbinary)
            if diagnostic3:
                print(
                    "Before length = ",
                    len(myAIS.AIS_Binary_Payload),
                    "\n",
                    myAIS.AIS_Binary_Payload,
                )
                print("addedbinary\n", addedbinary)
            myAIS.AIS_Binary_Payload = myAIS.AIS_Binary_Payload + addedbinary
            if diagnostic3:
                print(
                    "after length = ",
                    len(myAIS.AIS_Binary_Payload),
                    "\n",
                    myAIS.AIS_Binary_Payload,
                )
            # update fragment identifier for scan
            x += 1

        success = True

    """ Clean out ophan/expired records"""
    # either found not enough or we were successful
    # clean out the FragDict of expired/orphan fragments
    # cant do it in one pass - throws a sixze changed error
    # instead create a new temporary dictionary and then overwrite the original
    xyzzy = {}

    # print('prior cleanup length FragDict = ', len(FragDict))
    for key in FragDict:
        try:
            # print('length of FragDict[key] in cleanup ',len(FragDict[key]))
            # print(key, ' ',FragDict[key])
            if len(FragDict[key]) == 8:
                # print('len FCD = 8')
                rectime = FragDict[key][7]
                delta = (datetime.now() - rectime).total_seconds()
                if diagnostic3:
                    print(
                        "Checking received timne in handle3 fragments ",
                        rectime,
                        " difference ",
                        delta,
                    )

                if diagnostic3:
                    if FragDict[key][3] == aisfields[3]:
                        print(
                            "message nos match should delete",
                            FragDict[key][3],
                            aisfields[3],
                        )

                if (
                    delta < GlobalDefinitions.Global.FragDictTTL
                    and FragDict[key][3] != aisfields[3]
                ):
                    xyzzy[key] = FragDict[key]
                else:
                    if diagnostic3:
                        print("not copying ", FragDict[key])

        except:
            pass
        # delete the original FragDict\

    if xyzzy:
        del FragDict
        if diagnostic3:
            for key in xyzzy:
                print("deleteme now ", xyzzy[key])
        FragDict = xyzzy

        if diagnostic3:
            print("post cleanup length FragDict = ", len(FragDict))
        xyzzy.clear()

    """' return AISObject or NONE"""

    if success:
        # print(myAIS.AIS_Binary_Payload[0:37])
        return myAIS
    else:
        return None
