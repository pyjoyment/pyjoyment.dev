# The configuration of gunicorn, which it reads from the current directory
raw_env = ['PYJO_WSGI=1', 'PYJO_MODE=production', 'PYJO_REVERSE_PROXY=1']
wsgi_app = 'app:application'
bind = '0.0.0.0:8000'
workers = 4
accesslog = '-'
