from Pyjoyment.Lite import *

import time


# The code of a job, a helper, which an action and a command share
@helper('purge')
def purge(c, days=30):
    cutoff = time.time() - days * 86400
    old = [file for file in app.home.child('uploads').list() if file.stat().st_mtime < cutoff]
    for file in old:
        file.remove()
    c.app.log.info(f'Purged {len(old)} uploads older than {days} days')
    return len(old)


@get('/admin/purge')
def admin_purge(c):
    c.render(json={'purged': c.purge(int(c.param('days') or 30))})


app.start()
