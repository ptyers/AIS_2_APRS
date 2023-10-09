from resty import PathDispatcher
from wsgiref.simple_server import make_server, WSGIRequestHandler
from GlobalDefinitions import Global
import time
import sys
import datetime
from dns import reversename
from dns import resolver
from socket import socket, AF_INET, SOCK_STREAM
import GlobalDefinitions
from SendAPRS import do_print_server_address


class NoLoggingWSGIRequestHandler(WSGIRequestHandler):
    # supersedes the logging messages from the simple server
    def log_message(self, format, *args):
        if Global.LogServer:
            self.logging_message(format, *args)
        else:
            pass

    def logging_message(self, format, *args):
        sys.stderr.write(
            "%s - - [%s] %s\n"
            % (self.client_address[0], self.log_date_time_string(), format % args)
        )


class Statistics:

    def __init__(self):
        pass

    _hello_response = """\
    <html>
    <head>
    <title>Hello {name}</title>
    </head>
    <body>
    <h1>Hello {name}</h1>
    </body>
    </html>"""

    _ship_response = """\
    <html>
    <head>
    <style>
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    th, td {
      padding: 5px;
    }
    th {
      text-align: left;
    }
    </style>
    <title style = "text-align : center'" >AIS to APRS Known Vessels</title>
    </head>
    <body>

    <h1 style = "text-align : center">AIS to APRS Known Vessels</h1>
    <table  style = "width: 100%'">
    <th>Vessel</th><th>MMSI</th><th>Callsign</th><th></th>\
    <th>Vessel</th><th>MMSI</th><th>Callsign</th><th></th>\
    <th>Vessel</th><th>MMSI</th><th>Callsign</th><th></th>\
    <th>Vessel</th><th>MMSI</th><th>Callsign</th><th></th>\
    <th>Vessel</th><th>MMSI</th><th>Callsign</th><th></th>\
    <th>Vessel</th><th>MMSI</th><th>Callsign</th><th></th>
    """
    _stats_response_middle = """\
    <table  style = "width: 50%'">
    <th  style = "width : 20%; padding : 10px"> Frames Received</th>
    <th style = "width : 20% ; padding : 10px"> Frames Dropped</th>
    <th style = "width : 20% ; padding : 10px"> Frame Rate</th>
    <th style = "width : 20% ; padding : 10px"> Frames Sent</th>
    """

    _stats_response = """\
    <html>
    <head>
    <style>
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    th, td {
      padding: 10px;
    }
    th {
      text-align: left;
    }
    </style>
    <title style = "text-align : center'" >AIS to APRS Operational Statistics</title>
    </head>
    <body>

    <h1 style = "text-align : center">AIS to APRS Operational Statistics</h1>
    """
    _stats_response_middle = """\
    <table  style = "width: 50%'">
    <th  style = "width : 20%; padding : 10px"> Stream </th>
    <th style = "width : 20% ; padding : 10px"> Frames In </th>
    <th style = "width : 20% ; padding : 10px"> Frames Dropped </th>
    <th style = "width : 20% ; padding : 10px"> Frames per Min </th>
    <th style = "width : 20% ; padding : 10px"> Frames Out </th>
    """

    _station_response_head = """\
        <html>
    <head>
    <style>
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    th, td {
      padding: 10px;
    }
    th {
      text-align: left;
    }
    </style>
    <title style = "text-align : center'" >AIS to APRS Operational Statistics</title>
    </head>
    <body>
    <h2>UpTime {Uptime}</h2<p></p>
    <table style = "width: 50%">
    <th  style = "width : 30%; padding : 10px"> IP Address </th>
    <th  style = "width : 10% ; padding : 10px">Frames Received </th>
    <tr><td> </td> <td> </td></tr>

    """
    _station_response_tail = """\

    </body>
    </html>"""

    def do_stats(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/html")])
        params = environ["params"]
        s = (datetime.datetime.now() - Global.starttime).total_seconds()
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_c = " {:03}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        resp = self._stats_response
        resp = (
                resp
                + "<p><h2>Up Time "
                + uptime_c
                + " </h2><h2>Station "
                + Global.Station
                + "</h2></p>"
                + self._stats_response_middle
        )
        resp = resp + "<tr><td>UDP</td><td>{UFrames}</td><td>{UDropped}</td><td>{URate}</td></tr>".format(
            UFrames=Global.Statistics["Nr_UDP_Frames_RX"],
            UDropped=Global.Statistics["Nr_UDP_Frames_Dropped"],
            URate=Global.Statistics["Nr_UDP_Frames_permin"],
        )
        resp = resp + "<tr><td>Serial<td>{UFrames}</td><td>{UDropped}</td><td>{URate}</td></tr>".format(
            UFrames=Global.Statistics["Nr_Serial_Frames_RX"],
            UDropped=Global.Statistics["Nr_Serial_Frames_Dropped"],
            URate=Global.Statistics["Nr_Serial_Frames_permin"],
        )
        resp = resp + "<tr><td>APRS<td></td><td></td><td>{URate}</td><td>{AFrames}</td></tr>".format(
            URate=Global.Statistics["Nr_APRS_permin"],
            AFrames=Global.Statistics["Nr_APRS_TX"],
        )
        resp = (
                resp + "</table><p> </p><p><h2>Stations from which frames Received</h2></p>"
                       '<p></p><table style = "width : 40%;">'
                       '<th style = "width : 20%; padding : 10px" > IP Address </th>'
                       '<th style = "width : 20% ; padding : 10px" > Frames Received </th>'
        )
        for xx in Global.UDP_Received_IP_Addresses:
            resp = resp + "\n<tr><td>{IP}</td><td>{Frames}</td></tr>".format(
                IP=xx, Frames=Global.UDP_Received_IP_Addresses[xx]
            )
        resp = resp + "</table>" + self._station_response_tail
        yield resp.encode("utf-8")

    def do_stations(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/html")])
        params = environ["params"]
        resp = self._station_response_head
        for xx in Global.UDP_Received_IP_Addresses:
            resp = resp + "\n<tr><td>{IP}</td><td>{Frames}</td></tr>".format(
                IP=xx, Frames=Global.UDP_Received_IP_Addresses[xx]
            )

        resp = resp + " </table>" + self._station_response_tail
        yield resp.encode("utf-8")

    def get_name_from_ip(self, ip: str) -> str:
        addrs =  reversename.from_address(ip)
        return str(resolver.resolve(addrs, "PTR")[0])

    def do_ships(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/html")])
        params = environ["params"]
        rowcount = 0
        Rowsperpage = 20
        columncount = 0
        resp = self._ship_response + "<tr>"
        if len(Global.MyMap) > 0:

            for key in Global.MyMap:
                if columncount > 5:
                    resp = resp + "</td><tr>"
                    columncount = 0
                resp = resp + "\n<td>{Vessel}</td><td>{MMSI}</td><td>{Call}</td><td></td>".format(
                    Vessel=Global.MyMap[key].Name,
                    MMSI=key,
                    Call=Global.MyMap[key].Callsign,
                )
                columncount += 1

        resp = resp + "</table>" + self._station_response_tail
        yield resp.encode("utf-8")

    def hello_world(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/html")])
        params = environ["params"]
        resp = self._hello_response.format(name=params.get("name"))
        yield resp.encode("utf-8")

    def __init__(self):
        pass

    def loopstats(self):

        dispatcher = PathDispatcher()
        dispatcher.register("GET", "/stats", self.do_stats)
        dispatcher.register("GET", "/stations", self.do_stations)
        dispatcher.register("GET", "/ships", self.do_ships)
        dispatcher.register("GET", "/hello", self.hello_world)

        # launch basic server
        httpd = make_server(
            "", Global.WebPort, dispatcher, handler_class=NoLoggingWSGIRequestHandler
        )
        print(
            "AIS_APRS started\nWebport",
            Global.WebPort,
            "\n Options: - stats, stations, ships, hello\n",
            "Use http//:127.0.0.1:[Webport]/[option] to see whats happening",
        )

        try:
            if self.do_check_server():
                print("server address and server port being used are")
                do_print_server_address(GlobalDefinitions.Global.UseRemote)
        except Exception as e:
            print("Error - No valid APRS Server available\n%s", e)
            GlobalDefinitions.Global.CloseDown = True

        httpd.serve_forever()
        while True:
            time.sleep(0.1)

    def do_check_server(self):
        try:
            aprs_stream = socket(AF_INET, SOCK_STREAM)
        except OSError as e:
            raise RuntimeError(
                "Error creating socket in check server: %s\n" % e
            ) from e

        if GlobalDefinitions.Global.UseRemote:
            serveraddress = (
                GlobalDefinitions.Global.remoteEnd,
                int(GlobalDefinitions.Global.APRSPort),
            )
        else:
            serveraddress = (
                GlobalDefinitions.Global.ServerAddress,
                int(GlobalDefinitions.Global.APRSPort),
            )

        # Second try-except block -- connect to given host/port
        try:

            aprs_stream.connect(serveraddress)
        except ConnectionRefusedError as e:
            raise RuntimeError(
                "Connection Refused error in check server:\r\n'\
            ' Address %s Port %d\n\r %s"
                % GlobalDefinitions.Global.ServerAddress,
                GlobalDefinitions.Global.APRSPort,
                e,
            ) from e
        except ConnectionError as e:
            raise RuntimeError("Connection error in check server: %s'\n" % e) from e

        except TimeoutError as e:
            do_print_server_address(UseRemote)
            raise RuntimeError("Timeout error in check server: %s'\n" % e) from e

        except Exception as e:
            raise RuntimeError(
                "Unspecified Connection Error connecting to server in check server: '\r''\n %s '\n'\r"
                % e
            ) from e

        return True
