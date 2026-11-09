import Pyjo.Test.Pyjo

from Pyjo.Test import *
from Pyjoyment.Lite import *


@get('/')
def index(c):
    c.render(inline=PAGE, items=['Bread', 'Milk'])


PAGE = """
<!DOCTYPE html>
<html>
  <head><title>Shopping list</title></head>
  <body>
    <h1 class="title">Shopping list</h1>
    <ul id="items">
      % for item in items:
        <li><%= item %></li>
      % end
    </ul>
    <a href="/about">About</a>
  </body>
</html>
"""


t = Pyjo.Test.Pyjo.new()

# The elements of the page by their CSS selectors
t.get_ok('/').status_is(200).content_type_like(r'^text/html')
t.text_is('title', 'Shopping list').text_is('h1.title', 'Shopping list')
t.element_exists('ul#items').element_count_is('#items li', 2)
t.text_is('#items li:first-child', 'Bread').text_like('#items li:last-child', r'^Mil')
t.attr_is('a', 'href', '/about').element_exists_not('form')

# The DOM of the response, for what the assertions do not say
items = t.tx.res.dom().find('#items li').map('text').to_list()
is_deeply_ok(items, ['Bread', 'Milk'], 'items in their order')

done_testing()
