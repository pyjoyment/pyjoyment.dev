import Pyjoyment.Plugin

import time


class MyPlugins_Timing(Pyjoyment.Plugin.object):
    # Runs once, when the application loads the plugin
    def register(self, app, conf):
        name = conf.get('name', 'app')

        # A helper, which the controllers and the templates call
        app.helper('timing.elapsed', lambda c: time.perf_counter() - c.stash('timing.start'))

        # The hooks of each request: the start, and the header of the response
        app.hook('before_dispatch', lambda c: c.stash({'timing.start': time.perf_counter()}))
        app.hook(
            'after_dispatch',
            lambda c: c.res.headers.header('Server-Timing', f'{name};dur={c.timing.elapsed() * 1000:.3f}'),
        )


object = MyPlugins_Timing
