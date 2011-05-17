import re
from datetime import datetime


class BaseParser(object):
    """
    Base class not to be used directly.
    """
    pattern = None
    date_format = None
    date_ignore_pattern = None

    @classmethod
    def parse_line(cls, line):
        """
        Parse one line of the log file.
        """
        regex = re.compile(cls.pattern)
        m = regex.search(line)
        if m:
            data = m.groupdict()
            data = cls.post_process(data)
            if cls.date_format:
                data['time'] = cls.convert_time(data['time'])
            else:
                data['time'] = datetime.now()
            return data
        else:
            return {}

    @classmethod
    def convert_time(cls, time_str):
        """
        Convert date string to datetime object
        """
        if cls.date_ignore_pattern:
            time_str = re.sub(cls.date_ignore_pattern, '', time_str)
        return datetime.strptime(time_str, cls.date_format)

    @classmethod
    def post_process(cls, data):
        """
        Implement this in the subclass. Accept/return parsed data structure.
        """
        return data

class NginxRequestTimesParser(BaseParser):
    """
    Used to parse the following Nginx log format:

    log_format request_times 'IP=$remote_addr,
                              TL=$time_local,
                              DN=$host,
                              RQ=$request,
                              HR=$http_referer,
                              HU=$http_user_agent,
                              CS=$cookie_sessionid,
                              UT=$upstream_response_time,
                              RT=$request_time,
                              US=$upstream_status,
                              SC=$status';
    """
    date_format = "%d/%b/%Y:%H:%M:%S"
    date_ignore_pattern = r' -\d{4}'
    pattern = ''.join([
            r'^IP=(?P<ip>[^,]+),',
            r'TL=(?P<time>[^,]+),',
            r'DN=(?P<host>[^,]+),',
            r'RQ=(?P<request>[^,]+),',
            r'HR=(?P<http_referer>[^,]+),',
            # user agents have commas sometimes
            r'HU=(?P<http_user_agent>[^(,CS=)]+),',
            r'CS=(?P<cookie_sessionid>[^,]+),',
            r'UT=(?P<upstream_response_time>[^,]+),',
            r'RT=(?P<request_time>[^,]+),',
            r'US=(?P<upstream_status>[^,]+),',
            r'SC=(?P<status>[^,]+)$',
            ])

    @classmethod
    def post_process(cls, data):
        """
        Convert request string into http method and url
        """
        request_string = data['request']
        request_pattern = r'(?P<http_method>GET|HEAD|POST) (?P<url>\S+)'
        m = re.search(request_pattern, request_string)
        if m:
            newdata = m.groupdict()
            data.update(newdata)

        # If the upstream response was '-' then Nginx bailed out and didn't wait
        # Assume it's some high value
        if data['upstream_response_time'] == '-':
            data['upstream_response_time'] = '90'

        # Convert the times to floats
        for time_label in ['request_time', 'upstream_response_time']:
            data[time_label] = float(data[time_label])

        return data


def parse_line(line):
    """
    Parse one line and output a dictionary of the parsed values.
    """
    return NginxRequestTimesParser.parse_line(line)

def parse_file(fp):
    parsed_data = []
    with open(fp, 'r') as logfile:
        for line in logfile:
            data = parse_line(line)
            if len(data) == 0:
                # We hit the end of the file
                print data
                print line
            parsed_data.append(data)

    return parsed_data
