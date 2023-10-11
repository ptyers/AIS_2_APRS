"""
SNMPv1 TRAP with defaults
+++++++++++++++++++++++++

Send SNMPv1 TRAP through unified SNMPv3 message processing framework
using the following options:

* SNMPv1
* with community name 'public'
* over IPv4/UDP
* send TRAP notification
* with Generic Trap #1 (warmStart) and Specific Trap 0
* with default Uptime
* with default Agent Address
* with Enterprise OID 1.3.6.1.4.1.20408.4.1.1.2
* include managed object information '1.3.6.1.2.1.1.1.0' = 'my system'

Functionally similar to:

| $ snmptrap -v1 -c public demo.snmplabs.com 1.3.6.1.4.1.20408.4.1.1.2 0.0.0.0 1 0 0 1.3.6.1.2.1.1.1.0 s "my system"

For Reference
(mib-root (1) iso (1) org (3) dod(6) internet (1) snmpv2(6) snmpmodules (3) snmpmib (1) \
    snmpmibobjects (1) snmptraps (5) )
Cold Start '1.3.6.1.6.3.1.1.5.1'
Warm Start '1.3.6.1.6.3.1.1.5.2'

extra trap (non-standard)
Error Trap '1.3.6.1.6.3.1.1.5.6'


"""  #
from pysnmp.hlapi import *

iterator = sendNotification(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget(('192.168.80.3', 162)),
    ContextData(),
    'trap',
    NotificationType(
        ObjectIdentity('1.3.6.1.6.3.1.1.5.2')
    ).addVarBinds(
        ('1.3.6.1.6.3.1.1.4.3.0', '1.3.6.1.4.1.20408.4.1.1.2'),
        ('1.3.6.1.2.1.1.1.0', OctetString('my system'))
    ).loadMibs(
        'SNMPv2-MIB'
    )
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)


def main(self):
    pass


if __name__ == 'main':
    main()
