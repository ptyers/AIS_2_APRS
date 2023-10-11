def new_create_binary_payload(p_payload: str):
    # munging binary strings undedr python is a difficult exercise
    # method using a VERY large integer created by bit shifting 6 bat a time failed
    # #because the integer produced was TOO TOO large
    #
    # new approach
    # create a list of Bytes contaning eight bits each
    # the extract routines are going to be messier but thats what ypu get
    #
    # create an empty list of bytes
    binary = bytearray()
    # use extend() to add bytes when they have had their eight bits filled
    _binary_length = len(p_payload) * 6  # expected number of bits

    # test varaiable
    printdiag = False

    # print(' entering create binary payload expected number of bits = ',_binary_length,'\r\npayload = ',p_payload)

    # now build the payload
    pointer = int(0)
    _current_word = int(0)
    # for (int i = 0 i < p_payload.Length i++)
    currbyte = 0
    tempint = 0
    nrbits = 0
    for i in range(0, len(p_payload) + 1):
        if i < len(p_payload):

            if printdiag:
                print("in create binary payload ", len(p_payload), i)
            # iterate through the string payload masking to lower 6 bits
            xchar = p_payload[i]

            nibble = m_to_int(xchar) & 0x3F  # ensures only 6 bits presented
            if printdiag:
                print("nibble", bin(nibble))
            tempint = (tempint << 6) + nibble
            # tempint = tempint + nibble
            nrbits += 6
            if printdiag:
                print(
                    "got 6 bits now append them - tempint = {} nrbits = {}".format(
                        bin(tempint), nrbits
                    )
                )
            if nrbits >= 8:  # now have at least 8 bits to append to list
                # now extract the upper 8 bits from tempint
                nrbits = nrbits - 8  # NOTE this presumes a few things
                currbyte = tempint >> (nrbits)
                if printdiag:
                    ("current byte", bin(currbyte))
                binary.append(currbyte)
                if printdiag:
                    print(binary)
                # now mask off the upper 8 bits of tempint
                tempint = tempint & (2 ** (nrbits) - 1)
                if printdiag:
                    print("tempint after masking ", bin(tempint))
        else:

            # edge condition
            # we are processing the last character in p_payload and still have bits left over
            # need to bit stuff another byte
            if printdiag:
                print(
                    "last byte i= ",
                    i,
                    "len(p_payload) = ",
                    len(p_payload),
                    " nrbits = ",
                    nrbits,
                    " tempint = ",
                    bin(tempint),
                )

            if nrbits > 0:
                # grab another byte put left over bits into it
                # then bit stuff it by shifting to an eight bit boundary
                currbyte = tempint
                currbyte << (8 - nrbits)
                binary.append(currbyte)

        s = ""
        for x in binary:
            s = s + format(x, "08b")

    if printdiag:
        print(s)

    # print(' leaving create binary payload ', self._binary_payload, ' ', bin(self._binary_payload))
    return binary


def newer_create_binary_payload(p_payload: str):
    # based on using a supersized string rather than bytearray
    #
    printdiag = False
    #
    # define a null string
    binary = ""
    for i in range(0, len(p_payload)):
        if printdiag:
            print("in create binary payload ", len(p_payload), i)
        # iterate through the string payload masking to lower 6 bits
        xchar = p_payload[i]

        nibble = m_to_int(xchar) & 0x3F  # ensures only 6 bits presented
        if printdiag:
            print("nibble", bin(nibble))

        # now append the nible to the stream
        binary = binary + format(nibble, "06b")

        if printdiag:
            print(binary)

    return binary


def xm_to_int(parameter: str) -> int:
    # takes in a encoded string of variable length and returns positive integer
    # print('entering m_to_int parameter = ', parameter)
    my_int = int(0)
    my_byte = ord(parameter)
    # print(len(parameter), ' ',parameter, ' ', my_byte)

    if len(parameter) == 1:
        my_int = int(my_byte)
        # need to mask off the upper 2 bits

        if (my_int - 48) > 40:
            my_int = my_int - 56
        else:
            my_int = my_int - 48

        # print('myint ', my_int, ' binary myint ', bin(my_int))
    else:
        print("multiple characters not yet handled in m_to_int\r\n", sys.exc_info()[0])
        raise RuntimeError("In m_to_int\r\n")
        # multi character integer values are made up of 6 bit "bytes" in either signed or unsigned versions
    # print('Leaving m_2_int my_int = {} bin((my_int) = {}'.format(my_int,bin(my_int)))
    return my_int


def ExtractInt(self, startpos: int, blength: int):  # int
    # extracts an integer from the binary payload
    # use Binary_Item to get the actual bits
    return int(Binary_Item(startpos, blength))


def newer_ExtractInt(self, bitarray, startpos: int, blength: int):  # int
    # extracts an integer from the binary payload
    # use Binary_Item to get the actual bits
    return int(newer_Binary_Item(bitarray, startpos, blength))


def newer_Binary_Item(bitarray, startpos: int, blength: int) -> int:
    # newer version concept only
    # convert bitarray to a string, use string slicing to get bits
    # then con vert the slice to int using int(string,2)

    s = ""
    for x in bitarray:
        s = s + format(x, "08b")

    reqbits = s[startpos: startpos + blength - 1]

    return int(reqbits, 2)


def Binary_Item(bitarray, startpos: int, blength: int) -> int:
    # newer version of Binary_Item using the bytearray produced as binary payload
    # given a starting position and number of bits extracts a binary bit stream
    # from the array p_binary_payload[]
    # starting position is highest order bit of binary pasyload (ie big ended)
    # bits are stored modulo 8 with last byte bit stuffed with zeros
    #
    # bitarray is a bytearray of bits bit stuffed with zeroes in last byte representing the binary_payload
    #
    diagprint = True

    # uses modulo 8 and divide by eight to get location of byte in which start bit resides and bit position in that byte
    returnbits = int(0)
    startbyte = startpos / 8
    bitpos = startpos % 8
    endbyte = 0
    endbit = 0
    currentbyte = 0

    if diagprint:
        print(" in binary item extract")
        print(
            "startpos {} startbyte {} startbit {} endbyte {} endbit {}".format(
                startpos, startbyte, bitpos, endbyte, endbit
            )
        )
        s = ""
        for x in bitarray:
            s = s + format(x, "08b")

    returnbits = bitarray[startbyte] & (2 ** (8 - bitpos) - 1)
    # mask the returned word with LSBs representing startbit, startbit+1 etc
    # still working on case where endbit within same byte
    endpos = startpos + blength - 1
    endbyte = endpos / 8
    currentbyte = startbyte
    if (
            endbyte == startbyte
    ):  # within same byte shift returnbits right to make finish bit LSB
        returnbits = returnbits >> (8 - startpos - blength)
    else:
        # messier goes over byte boundary
        # have some bits already in returnbits
        # need to work out where end bit lives might be one or more bytes along
        currentbyte += 1
        while currentbyte < endbyte:  # shouldnt happen if currentbyte = endbyte
            # shift return bits up 8 bits and add in from current byte
            returnbits = returnbits << 8 + bitarray[currentbyte]
            currentbyte += 1

        # now for the bits left over in last byte
        endbit = endpos % 8  # how many bits to get from last byte starting at MSB
        lastbits = bitarray[currentbyte] >> (8 - endbit + 1)
        returnbits = returnbits << (endbit + 1) + lastbits

        if isinstance(returnbits, int):
            return returnbits
        else:
            return int(returnbits)


def extend_binary_payload(
        binarypayload, newpayload, oldlength: int, startpos: int, addlength: int
):
    """
    binarypayload and newpayload are each bitarrays of 8 bit bytes zero bit stuffed at LSB of last byte
    oldlength is nominal length in bits of original payload
    startpos is position which the new bitstring should be added
    addlength is how many more bits to add number of bits in newpayload less the zero bits stuffed at LSB last byte
    """
    # old payload finishes in byte origendbyte

    origendbyte = oldlength / 8
    oldorigbits = (
            oldlength % 8
    )  # which means there were 8-oldorigbits zero stuffed which must be replaced
    # sanity check the start bit position of the added payload should start at position oldorigbits+1 in last byte
    # and of course this should match the parameter startpos passed
    #
    newbytepos = 0
    if oldorigbits == 0:  # ends on a boundary - NICE
        startadd = startpos / 8
        endbyte = startpos + addlength - 1
        newbytepos = 0
        # just add bytes until you get to last byte
        while startadd <= endbyte:
            binarypayload.append(newpayload[newbytepos])
            newbytepos += 1
            # since the old payload ended on a bit boundary the last byte of newpayload can be directly placed
            # without the hassles of redoing bit stuffing
    else:
        """
        now its more messy
        we have a zero bit stuffed last byte of oldpayload
        into which we have to place some bits of the new payload
        need to mask off the appropriate MSBs in newpayload first byte and add them to the last byte of oldpayload
        then do a bit shuffle of all the other bits

        """
        tempint = int(0)
        # how many bits have been stuffed ?
        # we know oldorigbits  so can determine how many bits were stuffed
        stuffcount = 8 - oldorigbits
        tempint = newpayload[newbytepos] >> stuffcount
        startbyte = startpos / 8
        binarypayload[startbyte] = binarypayload[startbyte] + tempint
        # thats done now it gets messy
        startbyte += 1
        # first clear out the MSBs from byte[0] of new payload
        newpayload[newbytepos] = newpayload[newbytepos] & (
                2 ** (8 - stuffcount) - 1
        )  # masked to the unused bits
        tempint = 0
        tempint = tempint + newpayload[newbytepos]
        # prepare to get next bits from newpayload[1] and greater
        newbytepos += 1
        nrbits = 8 - stuffcount
        while startbyte < (startpos + addlength) / 8:
            tempint = tempint + newpayload[newbytepos]
            nrbits += 8
            # have now got more than 8 bits in tempint
            # grab the 8 MSB and append to binarypayload
            if nrbits > 8:
                # mask off upper 8 bits with LSB at nrbits-8 by right shifting
                #
                newpayload[newbytepos].append(tempint >> (8 - nrbits))
                newbytepos += 1
                nrbits -= 8  # reducve bit count by 8
                tempint = (
                                  tempint & (2 ** (8 - nrbits) - 1)
                          ) << 8  # mask to nrbits and shift up 8

            # now working on last bits which do notr make up a full byte
            # from previous whiule have tempint containg some bits upshifted 8
            # we need to append the left over bits from newpayload to this tempint
            # with MSB of new payload at position 7 (little ended)
            #
            # first we need to downshift the tempint by 8 since we are not adding a full 8 bit byte
            tempint = tempint >> 8
            # shift the newpayload byte rightwards to get only relevant bits
            remainder = (
                                startpos + addlength - 1
                        ) % 8  # the remainder mod 8 is number of bits yto be used
            tempbyte = newpayload[newbytepos] >> (8 - remainder)
            # there exists a posibility that the sum of nrbits plus left over may be more than eight
            # so the usual munging must occur
            if (nrbits + remainder) <= 8:
                # will fit into one byte left shift tempint by remainder bits and add in the new bits
                tempint = (tempint << remainder) + tempbyte
                # now zero bit stuff the tempint (potential byte) to 8 bits
                tempint = tempint << (8 - (nrbits + remainder))
                # left shift tempbyte to line up MSB with position in tempint
                # by default this zero bit stuffs the last byte
                # )
                binarypayload[newbytepos].append(tempint + tempbyte << 8 - nrbits)

            else:
                # need to fill byte and add one more zero stuffed
                # need to grab sufficient MSB bits from temp byte to make up a complete byte
                # append that byte then use leftover bits to MSB fill a new byte
                # left shift tempint by remainder bits
                tempint = tempint << remainder + tempbyte
                # extract the MSB eight bits of tempint and append to binary list
                binarypayload[newbytepos].append(tempint << (nrbits + remainder - 8))
                newbytepos += 1
                # now mask thew remaining bits in tempint and left shift them to MSB position
                rightbits = nrbits + remainder - 8
                binarypayload[newbytepos].append(
                    (tempint & (2 ** rightbits - 1)) << (8 - rightbits)
                )

        return binarypayload


def main(self):
    pass


if __name__ == 'main':
    main()
