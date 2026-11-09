import Pyjo.Exception
import Pyjo.Promise

from Pyjoyment.Lite import *


# Two services at the same time, within two seconds, while the server goes on with the other requests
@get('/pyjoyment')
async def pyjoyment(c):
    pypi = c.ua().get_p('https://pypi.org/pypi/Pyjoyment/json')
    github = c.ua().get_p('https://api.github.com/repos/pyjoyment/Pyjoyment')
    try:
        (pypi_tx,), (github_tx,) = await Pyjo.Promise.race(
            Pyjo.Promise.all(pypi, github), Pyjo.Promise.timeout(2, 'Too slow')
        )
    except Pyjo.Exception.object as e:
        return c.render(json={'error': e.message}, status=504)

    c.render(
        json={
            'version': pypi_tx.result.json('/info/version'),
            'stars': github_tx.result.json('/stargazers_count'),
        }
    )


app.start()
