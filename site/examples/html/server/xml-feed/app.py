"""
__DATA__

@@ feed.xml.ep
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>News</title>
  <id><%= url_for('feed').to_abs() %></id>
  <updated><%= posts[0]['date'] %>T00:00:00Z</updated>
  % for post in posts:
  <entry>
    <title><%= post['title'] %></title>
    <id><%= url_for('post', id=post['id']).to_abs() %></id>
    <link href="<%= url_for('post', id=post['id']).to_abs() %>"/>
    <updated><%= post['date'] %>T00:00:00Z</updated>
  </entry>
  % end
</feed>
"""

from Pyjoyment.Lite import *


posts = [
    {'id': 2, 'title': 'Templates & XML', 'date': '2026-11-09'},
    {'id': 1, 'title': 'Hello World', 'date': '2026-11-01'},
]


# /feed.xml, whose format renders feed.xml.ep, with the Content-Type of XML, and escapes the values
@get('/feed', format=['xml'], name='feed')
def feed(c):
    c.render('feed', posts=posts)


@get('/posts/<id:num>', 'post')
def post(c):
    c.render(text=next(post['title'] for post in posts if post['id'] == int(c.param('id'))))


app.start()
