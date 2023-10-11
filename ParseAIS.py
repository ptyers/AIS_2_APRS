import AISData
import Fragment
import MyPreConfigs
import GlobalDefinitions


# region ParseAIS
def Parse_AIS(self, returnData: str, pre_validated: bool):
    diagnostic = MyPreConfigs.diagnostic
    diagnostic2 = MyPreConfigs.diagnostic2
    diagnostic3 = MyPreConfigs.diagnostic3

    x = Fragment
    MyFrags = []  # list used within function

    try:

        if len(returnData) > 8:
            if returnData[0:1] == "!":
                pre_validated = True

        #  prevalidate the input string to at least 8 chars and start with "!"
        if pre_validated:
            if diagnostic2 or diagnostic3:
                print(
                    "pre_validated returndata.length = "
                    + str(len(returnData))
                    + " "
                    + returnData
                )

            #  now start analysing the data received
            # if (Convert.ToInt16(returnData[7: 1]) == 1)
            if int(returnData[7:1]) == 1:
                try:
                    #  non-fragmented message
                    #  Console.WriteLine("Non Fragmented")
                    # AIS_Data newdata = new AIS_Data(returnData)
                    # newdata = AISData.AIS_Data(returnData)
                    newdata = AISData.AIS_Data()
                    mydata = newdata
                    #  Console.WriteLine("Checking AVCGA")
                    try:
                        if mydata.String_MMSI in GlobalDefinitions.Global.AVCGADict:
                            mydata.isAVCGA = True

                    # catch (Exception e)
                    except Exception as e:
                        del newdata
                        raise RuntimeError(
                            "Exception while checking AVCGA string = "
                            + mydata.String_MMSI
                            + "\n\r",
                            e,
                        ) from e
                except Exception as e:
                    raise RuntimeError(
                        "Exception while Working Non-fragmented", e
                    ) from e

            #  if nonfragmented (fragment count =1)
            else:
                try:
                    if diagnostic2:
                        print("Fragmented data")
                    #  fragmented message
                    myfrag = Fragment.FRAGMENT(returnData)

                    if myfrag.IntFragNo == 1:
                        try:
                            #  first fragment
                            #  create an array of fragments with IntFragCount entries
                            MyFrags.append(myfrag)
                        except Exception as e:
                            raise RuntimeError("Error in first fragment", e) from e
                        #  if fragment number 1
                    else:
                        try:
                            #  multi part fragment second or later fragment
                            if myfrag.IntFragNo < (myfrag.IntFragCount):
                                MyFrags[myfrag.IntFragNo - 1] = myfrag
                            else:
                                #  need to fill the last array entry: before aggregating
                                MyFrags[myfrag.IntFragNo - 1] = myfrag
                                #  second or later fragment
                                #  if fragno equals frag count can process
                                if myfrag.IntFragNo == myfrag.IntFragCount:
                                    #  now have got all the fragments
                                    #  need to aggregate the payloads
                                    #  hopefully the first will have no fill bits and ditto the second etc in multipart fragements
                                    #  only the last should have fill bits.
                                    #  now combine the payload field of fragment one and two then the aggreagated payload one with three etc
                                    #  allowing for fill bits which existed in frag 1/2/3 etc (if any)
                                    # for (int i = 1 i < myfrag.IntFragCount i++)

                                    ix = 1
                                    while ix < myfrag.IntFragCount:
                                        MyFrags[0].PayLoad = self.Mergefragments(
                                            MyFrags[0], MyFrags[ix]
                                        )
                                        ix += 1

                                #  now create the AIS_Data object
                                newdata = AISData.AIS_Data()
                                GlobalDefinitions.Global.mydata = newdata
                                del newdata
                                del myfrag
                        except Exception as e:
                            raise RuntimeError("Error in later fragments", e) from e
                except Exception as e:
                    raise RuntimeError("In Parse Failed merging fragments", e) from e
        else:
            if diagnostic3:
                print("In parsing data too short < 8 bytes")

    except Exception as e:
        raise RuntimeError("Exception while parsing in send data", e) from e


def main(self):
    pass


if __name__ == 'main':
    main()
