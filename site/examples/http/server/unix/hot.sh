# A manager of prefork in the background, with its workers
pyjo-hot app.py

# A deployment with zero downtime: the same command starts new workers with the new code, and stops the old ones once
# they finish their requests
git pull
pyjo-hot app.py

# A graceful stop
pyjo-hot -s app.py
