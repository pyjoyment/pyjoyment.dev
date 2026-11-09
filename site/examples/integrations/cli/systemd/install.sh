sudo cp myapp.socket myapp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now myapp.socket

curl http://127.0.0.1:8080/   # the first request starts the service

# A new version, whose requests wait in the backlog of the socket while the workers restart
git pull
sudo systemctl restart myapp

journalctl -u myapp -f
