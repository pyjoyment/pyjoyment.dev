import Pyjo.UserAgent


ua = Pyjo.UserAgent.new(max_redirects=5)
dom = ua.get('https://pyjoyment.readthedocs.io/').result.dom()

# The title of the page, the text of its first heading, and the first targets of its links
print(dom.at('title').text)
print(dom.at('h1').all_text)
for href in dom.find('a[href]').map('attr', 'href').head(5):
    print(href)
