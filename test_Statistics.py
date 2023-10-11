from unittest import TestCase
from Statistics import Statistics
from dns import resolver


class TestStatistics(TestCase):
    def test_get_name_from_ip(self):
        mystat = Statistics

        name = mystat.get_name_from_ip(mystat, "127.0.0.1")
        self.assertEqual(name, "localhost.", "Incorrect name returned")
        name = mystat.get_name_from_ip(mystat, "8.8.8.8")
        self.assertEqual(name, "dns.google.", "Incorrect name returned")


def main(self):
    pass


if __name__ == 'main':
    main()
