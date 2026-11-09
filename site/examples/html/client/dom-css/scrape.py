import Pyjo.UserAgent


ua = Pyjo.UserAgent.new()
dom = ua.get('https://pyjoyment.dev').result().dom()

# The text of the first heading, and the targets of the links
print(dom.at('h1').all_text())
for link in dom.find('a[href]'):
    print(link['href'])
