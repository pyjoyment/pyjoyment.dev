# A service account of Google that publishes to the topic, which the service account of Kubernetes of the annotation
# acts as
gcloud iam service-accounts create publisher
gcloud pubsub topics add-iam-policy-binding events --role roles/pubsub.publisher \
  --member serviceAccount:publisher@myproject.iam.gserviceaccount.com
gcloud iam service-accounts add-iam-policy-binding publisher@myproject.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser --member 'serviceAccount:myproject.svc.id.goog[default/myapp]'

# Or Workload Identity Federation for GKE, without a service account of Google nor the annotation: the role goes to the
# principal of the service account of Kubernetes, of the number of the project
gcloud pubsub topics add-iam-policy-binding events --role roles/pubsub.publisher \
  --member principal://iam.googleapis.com/projects/123456789012/locations/global/workloadIdentityPools/myproject.svc.id.goog/subject/ns/default/sa/myapp

# The image of the application, and the pods
uv run app.py generate dockerfile
gcloud builds submit --tag europe-west1-docker.pkg.dev/myproject/apps/myapp
kubectl apply -f kubernetes.yaml
