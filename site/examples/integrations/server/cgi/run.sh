chmod +x cgi-bin/*
python app.py daemon

curl http://127.0.0.1:3000/cgi-bin/uptime.sh
curl -d name=Sara http://127.0.0.1:3000/cgi-bin/form.pl
