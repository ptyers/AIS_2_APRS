"""
using System_destination
using System.Collections_destination
using System.Collections.Generic_destination
using System.Collections.Specialized_destination
using System.Linq_destination
using System.Text_destination
using System.Threading_destination
using System.Threading.Tasks_destination
using System.Net_destination
using System.Net.Sockets_destination
using System.diagnostics_destination
using System.IO_destination
using System.Windows.Forms_destination

namespace AIS_APRS2
"""


class MergeFragments:

    # region MergeFragments
    def Mergefragments(self, Frag1, Frag2):
        # parameters are type FRAGMENT

        frag1 = Frag1
        frag2 = Frag2
        if frag1.FillBits == 0:
            #  no fill bits used - can concatenate the payload strings without bit munching
            #
            frag1.PayLoad = frag1.PayLoad + frag2.PayLoad
            #  now can initialise AIS_Data with the newly encoded informatoion.
            #
            return frag1.PayLoad

        else:
            #  NOW IT GETS COMPLICATED
            #  NEED TO shuffle bits allowing for the fill bits inserted
            #
            holder = 0

            holder2 = 0

            f1payload = frag1.PayLoad

            lastchar = f1payload[len(f1payload) - 1: 1]

            f1payload = f1payload[0: len(f1payload) - 2]

            #
            #  now convert the last character and the second payload to bytes
            mybyte = bytearray(lastchar, "utf-8")  # will only be 1 element
            mybyte2 = bytearray(frag2.PayLoad, "utf-8")  # multiple elements

            #  now mask off lower bits in last char
            holder = mybyte[0]  # should be a single byte
            holder = holder >> frag1.FillBits
            holder = holder << frag1.FillBits  # now zero filled at lower bits
            #  now for the byte array of characters from the second fragment we need to grab frag1.FillBits of the MSBs
            #  and add them to the preceding byte starting from mbyte[0]etc
            i = 0
            # for (int i = 0 i < mybyte2.Length i++)
            while i < len(mybyte2):
                if i == 0:
                    #  cross over from mybyte to mybyte2
                    holder2 = mybyte2[i]
                    holder2 = holder2 & 0x3F
                    holder2 = holder2 >> frag1.FillBits
                    holder = holder + holder2
                    mybyte[0] = holder
                else:
                    if i < len(mybyte2) - 1:
                        holder = mybyte2[i - 1]
                        holder2 = mybyte2[i]
                        holder = holder >> frag1.FillBits
                        holder = (
                                holder << frag1.FillBits
                        )  # now zero filled at lower bits
                        holder2 = holder2 >> frag1.FillBits
                        holder = holder + holder2
                        mybyte2[i - 1] = holder

                    else:
                        #  last byte in second fragment payload
                        #  will need be filled with trailing zeroes
                        #  after we tweak second last byte
                        holder = mybyte2[i - 1]
                        holder2 = mybyte2[i]
                        holder = holder >> frag1.FillBits
                        holder = (
                                holder << frag1.FillBits
                        )  # now zero filled at lower bits
                        holder2 = holder2 >> frag1.FillBits
                        holder = holder + holder2
                        mybyte2[i - 1] = holder
                        #  now the last byte
                        holder2 = mybyte2[i]
                        holder2 = holder2 << frag1.FillBits
                        #  the fillbits count remains constant for fragment 1 after the aggregation

                #  now covert the byte arrays back to strings and concatenate
                # lastchar = Encoding.ASCII.GetString(mybyte)
                lastchar = str.decode(mybyte, "utf-8")
                # secondstring = Encoding.ASCII.GetString(mybyte2)
                secondstring = str.decode(mybyte2, "utf-8")

            frag1.PayLoad = frag1.PayLoad + lastchar + secondstring

            return frag1.PayLoad  # returns a FRAGMENT


def main(self):
    pass


if __name__ == 'main':
    main()
