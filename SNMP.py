"""
Simple Network Management Agent

code yet to be written

planned
Will produce a trap on exceptions
Will respond to GET commands returning statistics, ships and stations as required

"""

from pysnmp.hlapi import sendNotification
from pysnmp.hlapi import SnmpEngine
from pysnmp.hlapi import UdpTransportTarget
from pysnmp.hlapi import ContextData
from pysnmp.hlapi import NotificationType
from pysnmp.hlapi import ObjectIdentity
from pysnmp.hlapi import OctetString
from pysnmp.hlapi import CommunityData


class SNMP:
    def __init__(self):
        pass


"""
Custom SNMPv1 TRAP
++++++++++++++++++

Send SNMPv1 TRAP through unified SNMPv3 message processing framework.

Original v1 TRAP fields are mapped into dedicated variable-bindings,
(see `RFC2576 <https://www.ietf.org/rfc/rfc2576.txt>`_) for details.

* SNMPv1
* with community name 'public'
* over IPv4/UDP
* send TRAP notification
* with Generic Trap #6 (enterpriseSpecific) and Specific Trap 432
* overriding Uptime value with 12345
* overriding Agent Address with '127.0.0.1'
* overriding Enterprise OID with 1.3.6.1.4.1.20408.4.1.1.2
* include managed object information '1.3.6.1.2.1.1.1.0' = 'my system'

Functionally similar to:

| $ snmptrap -v1 -c public demo.snmplabs.com 1.3.6.1.4.1.20408.4.1.1.2 127.0.0.1 6 432 12345 1.3.6.1.2.1.1.1.0 s "my system"

"""


def sendtrap(
    community="public",
    mpmodel=0,
    snmpmanager="102.168.80.3",
    snmpport=162,
    objectid="1.3.6.1.2.1.1.5",
    **varbinds
):
    print("about to send")
    iterator = sendNotification(
        SnmpEngine(),
        CommunityData(community, mpmodel),
        UdpTransportTarget((snmpmanager, snmpport)),
        ContextData(),
        "trap",
        NotificationType(ObjectIdentity(objectid))
        .addVarBinds(
            ("1.3.6.1.2.1.1.3.0", 12345),
            ("1.3.6.1.6.3.18.1.3.0", "127.0.0.1"),
            ("1.3.6.1.6.3.1.1.4.3.0", "1.3.6.1.4.1.65000.4.1.1.2"),
            ("1.3.6.1.2.1.1.1.0", OctetString("my system")),
        )
        .loadMibs("SNMPv2-MIB", "SNMP-COMMUNITY-MIB"),
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)


if __name__ == "__main__":
    print ("run as main")
    sendtrap('public', 0, '192.168.80.3', 162, "1.3.6.1.6.3.1.1.5.6")
else:
    print("not main")
