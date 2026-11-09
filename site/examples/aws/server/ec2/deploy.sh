# The instance profile of the role of the application, and IMDSv2 only, whose token Pyjo-AWS takes
aws ec2 associate-iam-instance-profile --instance-id i-0123456789abcdef0 --iam-instance-profile Name=myapp
aws ec2 modify-instance-metadata-options --instance-id i-0123456789abcdef0 --http-tokens required

# On the instance: Pyjo-AWS of the script in a virtual environment, and the service of systemd
cd /opt/myapp
uv venv && VIRTUAL_ENV=/opt/myapp/.venv uv sync --script app.py --active
sudo cp myapp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now myapp
