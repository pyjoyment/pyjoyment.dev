import Pyjo.Test.Pyjo

from Pyjo.Test import *
from Pyjoyment.Lite import *


# The extension is optional, with the format of Accept without it
@get('/report', {'format': None}, format=['json', 'txt'])
def report(c):
    c.respond_to(json={'json': {'total': 1}}, txt={'text': 'total: 1'})


@get('/old')
def old(c):
    c.redirect_to('/report.json')


@get('/cookie')
def cookie(c):
    c.cookie('seen', 'yes')
    c.render(text=f'seen: {c.cookie("seen") or "no"}')


t = Pyjo.Test.Pyjo.new()

with subtest('Content negotiation'):
    t.get_ok('/report.json').status_is(200).content_type_like(r'^application/json').json_is('/total', 1)
    t.get_ok('/report.txt').status_is(200).content_type_like(r'^text/plain').content_is('total: 1')
    t.get_ok('/report', {'Accept': 'application/json'}).status_is(200).json_is('/total', 1)

with subtest('Redirects'):
    t.get_ok('/old').status_is(302).header_like('Location', r'/report\.json$')
    t.ua.max_redirects = 1
    t.get_ok('/old').status_is(200).json_is('/total', 1)

# The test object keeps the cookies, as a browser does
with subtest('Cookies'):
    t.get_ok('/cookie').status_is(200).content_is('seen: no')
    t.get_ok('/cookie').status_is(200).content_is('seen: yes')

done_testing()
