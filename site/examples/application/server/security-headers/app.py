"""
__DATA__

@@ index.html.ep
<!DOCTYPE html>
<html>
  <head>
    <title>Welcome</title>
    %= stylesheet('/app.css')
    %= javascript(begin
      document.addEventListener('DOMContentLoaded', () => console.log('Welcome!'));
    %= end)
  </head>
  <body><h1>Welcome</h1></body>
</html>
"""

from Pyjoyment.Lite import *


# The headers of every response: HSTS over HTTPS, a strict policy tried out with the reports of the browsers while the
# default one is enforced, and the features that the pages do not use
plugin(
    'SecurityHeaders',
    hsts={'max_age': 300},
    csp_report_only={
        'default-src': ["'self'"],
        'img-src': ["'self'", 'data:'],
        'frame-ancestors': ["'none'"],
    },
    permissions={'camera': [], 'geolocation': [], 'microphone': [], 'fullscreen': ['self']},
    reports='/csp-reports',
)


# The inline script of the template has the nonce of the response, which the policy allows
@get('/')
def index(c):
    c.render('index')


# The violations, which the plugin logs, kept elsewhere too
@hook('csp_report')
def report(c, report):
    c.app.log.info(f'{report["effectiveDirective"]} blocked {report["blockedURL"]}')


app.start()
