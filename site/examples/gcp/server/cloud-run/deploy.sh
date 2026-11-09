# A server on http://127.0.0.1:3000, with the credentials of gcloud auth application-default login
uv run app.py daemon

# Dockerfile and .dockerignore, of the dependencies of the script, with prefork on the PORT that Cloud Run sets, and a
# graceful timeout under the 10 seconds that Cloud Run gives a container to stop
uv run app.py generate dockerfile --graceful-timeout 8

# The image, of Cloud Build, and the service of service.yaml
gcloud builds submit --tag europe-west1-docker.pkg.dev/myproject/apps/myapp
gcloud run services replace service.yaml --region europe-west1
