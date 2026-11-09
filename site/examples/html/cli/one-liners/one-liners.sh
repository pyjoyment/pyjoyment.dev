# The text of an element of a page, by its CSS selector
pyjo get https://pyjoyment.dev 'title' text

# The targets of its links, following the redirects
pyjo get -r https://pyjoyment.readthedocs.io/ 'a.reference.internal' attr href

# HTML of the standard input, with the functions of python -m Pyjo
curl -sL https://pyjoyment.dev | python -m Pyjo 'x(s()).at("title").text'

# HTML of the command line
python -m Pyjo 'x("<p>Hello <b>World</b></p>").at("b").text'
