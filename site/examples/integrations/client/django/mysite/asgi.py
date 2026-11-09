import Pyjo.Server.ASGI

from Pyjo.File import curfile

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django = get_asgi_application()

# The application of realtime.py next to manage.py, as an ASGI application
pyjo = Pyjo.Server.ASGI.new()
pyjo.load_app(curfile().dirname().sibling('realtime.py'))
realtime = pyjo.to_asgi_app()


# Pyjoyment under /realtime, whose URLs have the prefix of root_path, and its lifespan, which Django does not have;
# Django for the rest
async def application(scope, receive, send):
    if scope['type'] == 'lifespan':
        return await realtime(scope, receive, send)
    if scope['path'] == '/realtime' or scope['path'].startswith('/realtime/'):
        return await realtime({**scope, 'root_path': scope.get('root_path', '') + '/realtime'}, receive, send)
    await django(scope, receive, send)
