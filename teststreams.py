# collection of test streams to allow testing of conversionfrom ais stream to an APRS stream

class TestStreams:



    def __init__(self):
        self.teststream = {
            1: ('!AIVDM,1,1,,A,17Ol>07?ldELk71b1h04i3v00000,0*5',
                'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                '3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n', '503123456'),
            2: ('!AIVDM,1,1,,A,17Ol>07?ldELk71b1h04i3v00000,0*5',
                'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                '3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n', '503123456'),
            3: ('!AIVDM,1,1,,A,17Ol>07?ldELk71b1h04i3v00000,0*5',
                'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                '3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n', '503123456'),
            4: ('!AIVDM,1,1,,A,47Ol>01vNlabtELk71b1h0000000,0*5',
                'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                '3823.99S\\14730.00WL\n', '503123456'),
            5: ('!AIVDM,1,1,,A,57Ol>000Bm`MHsCGH01@E=B1AU0GF1HE=<Dh000U6@g<=2m<DI3AC000000000000000000,0*5',
                'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                '0000.00S\\00000.00Ws360.0/0.0 503123456 \n', 'VN456'),
            9: ('!AIVDM,1,1,,A,97Ol>045DdELk71b1h04i0000000,0*5',
                'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                '3823.99S\\14730.00W^122.0/300 503123456 503123456\n', '503123456'),
            12: ('!AIVDM,1,1,,A,<7Ol>01ou3P0D89CP9CP1PC8?BDP144B5CC54PC165DIPD5HD0000000000000,0*5',
                 'CG722>APU25N,TCPIP*:503123456:THIS IS A SHORT ADDRESSED SAFETY TEXT\n', '503123456'),
            14: ('!AIVDM,1,1,,A,>7Ol>01@PU>0U>061@E=B1<4HEAV0lE=<4LD000000000000000000000,0*5',
                 'CG722>APU25N,TCPIP*::BLN0     :THIS IS A TEST SAFETY MESSAGE'),
            18: ('!AIVDM,1,1,,A,B7Ol>001;5G<ihJPL01<@wP00000,0*5',
                 'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                 '3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n', '503123456'),
            19: ('!AIVDM,1,1,,A,C7Ol>001;5G<ihJPL01<@wP0`:Va0d:VV:H000000000BS8GV6P0,0*5',
                 'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                 '3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n', '503123456'),
            21: ('!AIVDM,1,1,,A,E7Ol>03:2ab@0TR000000000000:fISPm0p00j5qQ`0003Sp1F51CTjCkP000,0*5',
                 'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                 '3823.99S\\14730.00Ws360.0/0.0 503123456 503123456\n', '503123456'),
            24: ('!AIVDM,1,1,,A,H7Ol>04U8@0L3>uF>lmn006@g<=0,0*5',
                 'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                '0000.00S\\00000.00Ws360.0/0.0 503123456 \n', 'VN456'),
            27: ('!AIVDM,1,1,,A,K7Ol>00bVC=<0?7`,0*5',
                 'CG722>APU25N,TCPIP*:;503123456*XXXXXXX'
                 '3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n', '503123456')
        }
    def __repr__(self):
        for key, items in self.teststream.items():
            print(f'Message TYpe {key}\n{items[0]}\n{items[1]}\n\n')


