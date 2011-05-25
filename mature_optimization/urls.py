from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mature_optimization.views',
    url(r'^$', 'dashboard',
         name='mature_optimization_dashboard'),

)