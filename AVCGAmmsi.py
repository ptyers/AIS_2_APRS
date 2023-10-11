"""
using System
using System.Collections
using System.Collections.Generic
using System.Collections.Specialized
using System.Linq
using System.Text
using System.Threading
using System.Threading.Tasks
using System.Net
using System.Net.Sockets
using System.diagnostics
using System.IO
using System.Windows.Forms
"""


class AVCGAMMSI:
    # hold data pertaining to an entry in the list of AVCGA vessels and their MMSIs
    # region Private Properties
    _facility = ""
    _location = ""
    _callsign = ""
    _stationType = ""
    _licenceNo = ""
    _siteID = ""
    _CGDom = ""
    _CGNewDom = ""
    _epirb = ""
    _hexNo = ""
    _expiry = ""
    _mmsi = ""
    _dsc = ""
    _ant_checked = ""
    _comment = ""

    # endregion
    # region Public Properties

    def Facility(self) -> str:
        return self._facility

    def Location(self) -> str:
        return self._location

    def Callsign(self) -> str:
        return self._callsign

    def StationType(self) -> str:
        return self._stationType

    def LicenceNo(self) -> str:
        return self._licenceNo

    def SiteID(self) -> str:
        return self._siteID

    def CGDomestic(self) -> str:
        return self._CGDom

    def CGNewDom(self) -> str:
        return self._CGNewDom

    def Epirb(self) -> str:
        return self._epirb

    def HexNo(self) -> str:
        return self._hexNo

    def Expiry(self) -> str:
        return self._expiry

    def MMSI(self) -> str:
        return self._mmsi

    def DSC(self) -> str:
        return self._dsc

    def AntennaChecked(self) -> str:
        return self._ant_checked

    def Comment(self) -> str:
        return self._comment

        # endregion
        # region Constructors

    def __init__(self, record: str):  # requires list of strings

        # constructor
        # takes array of strings and assigns to appropriate string variable

        _facility = record[0]
        _location = record[1]
        _callsign = record[2]
        _stationType = record[3]
        _licenceNo = record[4]
        _siteID = record[5]
        _CGDom = record[6]
        _CGNewDom = record[7]
        _epirb = record[8]
        _hexNo = record[9]
        _expiry = record[10]
        _mmsi = record[11]
        _dsc = record[12]
        _ant_checked = record[13]
        _comment = record[14]


def main(self):
    pass


if __name__ == 'main':
    main()
