import urlparse
from collections import namedtuple

PageRequest = namedtuple(
    'PageRequest',
    ['path', 'http_method', 'occurrences', 'total_time', 'avg_time'])

class SlowPages(object):
    def __init__(self, parsed_data, slow_threshold):
        self.parsed_data = parsed_data
        self.slow_threshold = slow_threshold
        self.pages = []

    def run(self):
        pages = {}
        for request in self.parsed_data:
            if request['upstream_response_time'] < self.slow_threshold:
                continue
            # Strip out any GET params from the url
            _, _, url, params_, _ = urlparse.urlsplit(request['url'])
            # Determine the key for this type of request
            req_key = (url, request['http_method'])
            if not pages.has_key(req_key):
                # Need to intialize the SlowPage for this type of request
                pr = PageRequest(
                    path=url,
                    http_method=request['http_method'],
                    occurrences=0,
                    total_time=0.0,
                    avg_time=0.0,
                )
            else:
                pr = pages[req_key]

            # Update the tuple, with an updated average
            new_occurrences = pr.occurrences + 1
            new_total_time = pr.total_time + request['upstream_response_time']
            pages[req_key] = PageRequest(
                path=pr.path,
                http_method=pr.http_method,
                occurrences=new_occurrences,
                total_time=new_total_time,
                avg_time=new_total_time / new_occurrences,
            )

        self.pages = list(pages.values())
