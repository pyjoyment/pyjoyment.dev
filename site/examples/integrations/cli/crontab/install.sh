# Once by hand, as cron runs it, which prints the number of the files
PYJO_MODE=production python app.py eval -v 'app.purge(days=7)'

crontab -l        # the jobs of the user, before
crontab crontab   # replaces them with the file
