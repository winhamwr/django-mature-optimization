
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response

@user_passes_test(lambda u: u.is_superuser)
def menu(request):
    context = dict()
    return render_to_response('mature_optimization/dashboard.html',
                              context, context_instance=RequestContext(request))
