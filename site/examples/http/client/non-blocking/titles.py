import Pyjo.Promise
import Pyjo.UserAgent

import sys


urls = sys.argv[1:] or [
    'https://pyjoyment.dev/',
    'https://pyjoyment.readthedocs.io/',
    'https://pypi.org/project/Pyjoyment/',
]
ua = Pyjo.UserAgent.new(max_redirects=5, request_timeout=20)


def title(tx):
    print(f'{tx.req.url}: {tx.result.dom().at("title").text}')


# Two requests at a time, each title as it comes, and the script waits for the last one
promise = Pyjo.Promise.map(lambda url: ua.get_p(url).then(title), *urls, concurrency=2)
promise.catch(lambda err: sys.exit(f'Failed: {err}')).wait()
