==================================================================
 Django-Mature-Optimization- Optimize According to Production Pain
==================================================================

:Web: http://github.com/winhamwr/django-mature-optimization
:Source: http://github.com/winhamwr/django-mature-optimization/source/
:Author: Wes Winham (@weswinham)

--

Overview
========

Django-Mature-Optimization is a tool to guide your towards optimizing the areas
of your application where you can get the most bang for your buck. It helps you
analyze your real production django usage and find the pages that are the most
painful for your users, your webserver and your database.

Django-Mature-Optimization:

* Parses your production logs and groups the data by URL.
* Gives you tables weighted by URL popularity and slow loading times so
  that you know exactly where you should be spending your time doing
  optimization.

What Django-Mature-Optimization Is *Not*
----------------------------------------

This project has *no* aspirations to do the following:
* Real-time log following/tailing. Projects like
  `Live Log Analyzer`_ are much more suited to that.
* Notifications or alerting. A `Nagios`_ or `Munin`_ plugin makes more sense.
* Long-Term trending. `Munin`_, `Cacti`_ etc. are all well-suited there.
* Profiling or analysis of a page once you've realized it's a priority.

The focus is on using a log source as the authoritative place for your
data and parsing that log source for the purpose of finding out which pages
are causing your users the most performance pain in production.

Requirements
============

You must be using a setup that allows you to produce a log file displaying
per-request URL + response time. Instructions are provided for Nginx as a
reverse proxy, but other options are possible.

You also must be using Django. Theoretically, there's nothing Django-specific
about most of this, but for now, it's all based on Django.

Installation
============

Install The Package
-------------------

Install the django-mature-optimization package::

    $ pip install -e git+git://github.com/winhamwr/django-mature-optimization.git@v0.0.2#egg=django-mature-optimization

Configure Your Django Project
-----------------------------

* Add ``mature_optimization`` to your django ``INSTALLED_APPS`` tuple.
* Include ``mature_optimization.urls`` in your root ``urls.py``. eg.::

    (r'^perf/', include('mature_optimization.urls')),

* In ``settings.py``, configure ``MO_REQUEST_TIMES_PATH`` to point to your log
  file.
* OPTIONAL: Set ``MO_SLOW_PAGE_SECONDS`` to the threshold at which you consider
  a page as "slow." The default is 7 seconds, but depending on your application,
  you might have a different definition.

Configure Nginx Logging
-----------------------

You'll need to configure Nginx to record the $upstream_response_time when
reverse proxying to your app server (mod_wsgi, fastcgi, gunicorn, etc.).
Currently, django-mature-optimization expects the following log format::

    log_format request_times 'IP=$remote_addr,TL=$time_local,DN=$host,RQ=$request'
        ',HR=$http_referer,HU=$http_user_agent,CS=$cookie_sessionid'
        ',UT=$upstream_response_time,RT=$request_time,US=$upstream_status,SC=$status';

The inside your ``server`` or ``location`` directive, use that log format as an
access log. For example::

    upstream my_upstream {
        server		127.0.0.1:8080;
        server		127.0.0.1:8080;
    }

    ### Reverse proxy to apache2/mod_wsgi ###
    location / {
        include	/etc/nginx/proxy.conf;

        proxy_pass http://my_upstream;

        access_log /var/log/nginx/request_times.log request_times;
    }

Note: You'll need to make sure that the user running your application (eg. the
  mod_wsgi user) has read access to the log file. On Debian-based linux, this
  can be accomplished by adding that user to the ``adm`` group::

    $ sudo adduser <my_wsgi_user> adm



.. _`Live Log Analyzer`: https://github.com/saltycrane/live-log-analyzer
.. _`Nagios`: http://www.nagios.org/
.. _`Munin`: http://munin-monitoring.org/
.. _`Cacti`: http://www.cacti.net/