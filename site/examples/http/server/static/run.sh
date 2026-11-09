DOCUMENT_ROOT=$PWD/site python app.py prefork -w 4 -l 'http://*:8080'

curl -I http://127.0.0.1:8080/
curl -H 'Range: bytes=0-99' http://127.0.0.1:8080/video.mp4
