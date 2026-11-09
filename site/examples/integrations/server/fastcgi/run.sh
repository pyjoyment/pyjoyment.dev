php-fpm -n -y php-fpm.conf -F &

python app.py daemon

curl http://127.0.0.1:3000/              # index.php
curl http://127.0.0.1:3000/hello/Sara    # index.php, with its own routes
curl http://127.0.0.1:3000/css/site.css  # the file, without PHP
