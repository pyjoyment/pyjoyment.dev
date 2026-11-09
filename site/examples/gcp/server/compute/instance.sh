# A service account of the instance, which reads the secret, and the secret itself
gcloud iam service-accounts create myapp
openssl rand -base64 32 | gcloud secrets create myapp-session --data-file=-
gcloud secrets add-iam-policy-binding myapp-session --role roles/secretmanager.secretAccessor \
  --member serviceAccount:myapp@myproject.iam.gserviceaccount.com

# The instance, whose metadata server gives the token of the service account of the scope of all the APIs, which its
# roles limit
gcloud compute instances create myapp-1 --zone europe-west1-b --machine-type e2-small \
  --service-account myapp@myproject.iam.gserviceaccount.com --scopes cloud-platform

# On the instance: the application, its dependencies and its unit of systemd
sudo useradd --system myapp
sudo uv venv /opt/myapp/.venv && sudo uv pip install --python /opt/myapp/.venv Pyjoyment Pyjo-GCP
sudo cp app.py /opt/myapp/ && sudo cp myapp.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now myapp
