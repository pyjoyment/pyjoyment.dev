import Pyjo.UserAgent

import sys


# Redirects followed, and limits of time, where the defaults wait longer
ua = Pyjo.UserAgent.new(max_redirects=5, connect_timeout=5, request_timeout=20)
ua.transactor.name = 'MyClient/1.0'

# result raises an exception for an error of the connection, but not for a response of an error, as 404
res = ua.get('https://pypi.org/pypi/Pyjoyment/json', {'Accept': 'application/json'}).result
if not res.is_success:
    sys.exit(f'{res.code} {res.message}')
print(res.json('/info/version'))

# A form, and JSON, with the response as JSON
print(ua.post('https://httpbin.org/post', form={'name': 'Sara'}).result.json('/form/name'))
print(ua.post('https://httpbin.org/post', json={'name': 'Sara'}).result.json('/json'))

# A file, saved as it comes
ua.get('https://pyjoyment.dev/pyjo/logo-black-4x.svg').result.save_to('logo.svg')
