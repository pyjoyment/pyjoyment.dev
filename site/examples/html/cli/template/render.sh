python render.py example.com 10.0.0.1:8080 10.0.0.2:8080 > /etc/nginx/conf.d/example.com.conf
nginx -t && nginx -s reload
