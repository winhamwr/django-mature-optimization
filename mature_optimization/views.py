
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext

from mature_optimization.parse import NginxRequestTimesParser
from mature_optimization.analyze import SlowPages

@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):

    parsed_data = NginxRequestTimesParser.parse_file(
        settings.MO_REQUEST_TIMES_PATH)
    slow_threshold = getattr(settings, 'MO_SLOW_PAGE_SECONDS', 7.0)
    slow_pages = SlowPages(parsed_data, slow_threshold)
    slow_pages.run()

    context = dict(
        slow_pages=sorted(
            slow_pages.pages, key=lambda x: x.total_time, reverse=True))
    return render_to_response('mature_optimization/dashboard.html',
                              context, context_instance=RequestContext(request))
