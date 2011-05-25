import datetime
import os.path
from unittest2 import TestCase

from mature_optimization.parse import parse_line, parse_file

FIXTURE_FP = os.path.join(
    os.path.dirname(__file__),
    '..',
    'fixtures',
    'two_minutes_csv.log')

class NginxLineParsingTestCase(TestCase):

    def test_simple_parse(self):
        data_string = (
            "IP=10.215.222.128,"
            "TL=17/May/2011:06:32:10 -0400,"
            "DN=foo.bar.com,"
            "RQ=POST /i/51764/lock/ HTTP/1.1,"
            "HR=https://foo.bar.com/i/confirm/51764/,"
            "HU=Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1,"
            "CS=7f40318ada63a2efc3bb693a184a89ac,"
            "UT=0.011,"
            "RT=0.403,"
            "US=403,"
            "SC=403\n")

        data = parse_line(data_string)

        self.assertEqual(
            data['time'],
            datetime.datetime(
                year=2011, month=5, day=17, hour=6, minute=32, second=10))
        self.assertEqual(data['url'], '/i/51764/lock/')
        self.assertEqual(data['request_time'], 0.403)

    def test_no_newline(self):
        data_string = (
            "IP=10.215.222.128,"
            "TL=17/May/2011:06:32:10 -0400,"
            "DN=foo.bar.com,"
            "RQ=POST /i/51764/lock/ HTTP/1.1,"
            "HR=https://foo.bar.com/i/confirm/51764/,"
            "HU=Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1,"
            "CS=7f40318ada63a2efc3bb693a184a89ac,"
            "UT=0.011,"
            "RT=0.403,"
            "US=403,"
            "SC=403")

        data = parse_line(data_string)

        self.assertEqual(
            data['time'],
            datetime.datetime(
                year=2011, month=5, day=17, hour=6, minute=32, second=10))
        self.assertEqual(data['url'], '/i/51764/lock/')
        self.assertEqual(data['request_time'], 0.403)


    def test_w_comma(self):
        # User agent has a comma
        data_string = (
            "IP=10.215.222.128,"
            "TL=17/May/2011:06:32:10 -0400,"
            "DN=foo.bar.com,"
            "RQ=POST /i/51764/lock/ HTTP/1.1,"
            "HR=https://foo.bar.com/i/confirm/51764/,"
            "HU=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.57 Safari/534.24,"
            "CS=7f40318ada63a2efc3bb693a184a89ac,"
            "UT=0.011,"
            "RT=0.403,"
            "US=403,"
            "SC=403\n")

        data = parse_line(data_string)

        self.assertEqual(
            data['time'],
            datetime.datetime(
                year=2011, month=5, day=17, hour=6, minute=32, second=10))
        self.assertEqual(data['url'], '/i/51764/lock/')
        self.assertEqual(data['request_time'], 0.403)

    def test_no_upstream_response(self):
        # When the upstream takes too long, Nginx returns a response quickly
        # and logs '-' as the upstream response
        data_string = (
            "IP=10.215.222.128,"
            "TL=17/May/2011:06:32:10 -0400,"
            "DN=foo.bar.com,"
            "RQ=POST /i/51764/lock/ HTTP/1.1,"
            "HR=https://foo.bar.com/i/confirm/51764/,"
            "HU=Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1,"
            "CS=7f40318ada63a2efc3bb693a184a89ac,"
            "UT=-,"
            "RT=0.403,"
            "US=403,"
            "SC=403\n")

        data = parse_line(data_string)

        self.assertEqual(
            data['time'],
            datetime.datetime(
                year=2011, month=5, day=17, hour=6, minute=32, second=10))
        self.assertEqual(data['url'], '/i/51764/lock/')
        self.assertEqual(data['request_time'], 0.403)
        # Default time is 90 seconds if they bail
        self.assertEqual(data['upstream_response_time'], 90.0)

class NginxFileParsingTestCase(TestCase):

    def test_basic_parse(self):
        parsed_data = parse_file(FIXTURE_FP)

        self.assertEqual(len(parsed_data), 14)

        # Ensure we have believable status codes
        for data in parsed_data:
            self.assertTrue(
                data['status'] in ['200', '403', '499'],
                "Status '%s' not in 200, 403 or 499" % data['status'])