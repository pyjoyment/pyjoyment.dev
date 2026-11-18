from Pyjoyment.Lite import *


# The pages of the frontend, also of its development server, read the API with the cookies of the session
ORIGINS = ['https://app.example.com', 'http://localhost:5173']
plugin('AllowedHosts', hosts=['api.example.com', 'localhost', '127.0.0.1'], origins=ORIGINS)
plugin('CORS', origins=ORIGINS, credentials=True, max_age=600, paths=['/api'])


@get('/api/user')
def user(c):
    c.render(json={'name': c.session('name')})


@post('/api/user')
def rename(c):
    c.session(name=c.req.json('/name'))
    c.render(json={'name': c.session('name')})


app.start()
