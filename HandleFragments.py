from  GlobalDefinitions import Global
from datetime import datetime
import AISData
import logging


def handle_fragments(payload):
    # payload id the tuple aisfields which is the AIS datastream
    # aisfields[5] is the actual payload, aisfields[1] is the fragment count
    # aisfields[2] is the fragment number of the sentence(payload)
    # aisfields[3] is the sequential message id to tie fragments together
    # aisfields[4] is the radio channel - not used in this module
    # returns True when all fragments found and merged
    # during processing will also flush out out dictionary entries older than preset amount

    FragdictTTL = Global.FragDictTTL

    diagnostic = Global.diagnostic
    diagnostic2 = Global.diagnostic2
    diagnostic3 = Global.diagnostic3

    aisfields = payload
    FragDict = Global.FragDict
    success = False  # used to determine if we return an AISOject or None
    deleteme = []

    logging.debug(" in handle_fragments payload =\r\n", payload)

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
    logging.debug("checking for matches")

    for key in Global.FragDict:  # scan through fragment numbers with common message number
        logging.debug(Global.FragDict[key], aisfields[1])
        try:
            testfrag = Global.FragDict[key]
            logging.debug(" finding matches testfrag ", testfrag)

            if testfrag[3] == aisfields[3]:  # matching message number
                logging.debug("match found", testfrag)

            ExtractedFrags[testfrag[2]] = testfrag
        except KeyError:
                logging.error("key error in checking")
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

        logging.debug("Have complete set of fragments")
        for x in ExtractedFrags:
            logging.debug("fragno {} Fragment {} ".format(int(x), ExtractedFrags[x]))

        """ If YES find fragment 1 and create AISObject"""

        try:
            aisfields = ExtractedFrags["1"]
        except KeyError as e:
            raise RuntimeError(
                "No fragment 1 in supposed full set of fragment", e
            ) from e
        logging.debug("creating AIS record myAIS")
        # create an AISObject from Fragment 1
        myAIS = AISData.AIS_Data(
            aisfields[0],
            aisfields[1],
            aisfields[2],
            aisfields[3],
            aisfields[4],
            aisfields[5],
            aisfields[6]
        )

        """ Loop through rest of fragments"""
        """     If necessary remove fill bits from fragment(current-1)"""
        """'    append binary list from current fragment"""
        logging.debug("about to scan records aisdfields[1] = ", int(aisfields[1]))
        x = 2
        while x <= int((aisfields[1])):  # from frag 2 to Fragcount
            testfrag = ExtractedFrags[str(x)]
            lastfrag = ExtractedFrags[str(x - 1)]
            logging.debug("testfrag ", testfrag)
            logging.debug(
                    "lastfrag ",
                    lastfrag,
                )
            # check if fill bits were used in previous fragment
            if lastfrag[6][0] != "0":  # fill bits were used
                # remove fill bits from myAIS.AIS_Binary_Payload
                # by slicing the string removing last fill chars bits
                myAIS.AIS_Binary_Payload = myAIS.AIS_Binary_Payload[
                                           0: -(int(lastfrag[6][0]))
                                           ]
                logging.debug("Fill bits removed\n", myAIS.AIS_Binary_Payload)
            # just append the binary string created from testfrag to myAIS.AIS_Binary_Payload
            addedbinary, addedlength = AISData.AIS_Data.create_binary_payload(
                testfrag[5]
            )
            logging.debug(addedbinary)
            logging.debug(
                    "Before length = ",
                    len(myAIS.AIS_Binary_Payload),
                    "\n",
                    myAIS.AIS_Binary_Payload,
                )
            logging.debug("addedbinary\n", addedbinary)
            myAIS.AIS_Binary_Payload = myAIS.AIS_Binary_Payload + addedbinary
            logging.debug(
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
    for key in Global.FragDict:
        try:
            # print('length of FragDict[key] in cleanup ',len(FragDict[key]))
            # print(key, ' ',FragDict[key])
            if len(Global.FragDict[key]) == 8:
                # print('len FCD = 8')
                rectime = Global.FragDict[key][7]
                delta = (datetime.now() - rectime).total_seconds()
                logging.debug(
                        "Checking received timne in handle3 fragments ",
                        rectime,
                        " difference ",
                        delta,
                    )

                if Global.FragDict[key][3] == aisfields[3]:
                    logging.debug(
                        "message nos match should delete",
                        Global.FragDict[key][3],
                        aisfields[3],
                    )

                if (
                        delta < Global.FragDictTTL
                        and Global.FragDict[key][3] != aisfields[3]
                ):
                    xyzzy[key] = Global.FragDict[key]
                else:
                    logging.debug("not copying ", Global.FragDict[key])

        except:
            pass
        # delete the original FragDict\

    if xyzzy:
        del Global.FragDict
        for key in xyzzy:
            logging.debug("deleteme now ", xyzzy[key])
        Global.FragDict = xyzzy

        logging.debug("post cleanup length Global.FragDict = ", len(Global.FragDict))
        xyzzy.clear()

    """' return AISObject or NONE"""

    if success:
        # print(myAIS.AIS_Binary_Payload[0:37])
        return myAIS
    else:
        return None


def main():
    pass


if __name__ == 'main':
    main()
