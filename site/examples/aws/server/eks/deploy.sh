# The image of the application, with its pre-forking server and Pyjo-AWS of the script
uv run app.py generate dockerfile
docker build -t 123456789012.dkr.ecr.eu-central-1.amazonaws.com/files:1.0 .
docker push 123456789012.dkr.ecr.eu-central-1.amazonaws.com/files:1.0

# EKS Pod Identity, instead of the annotation of IRSA: its agent, and the role of the service account
aws eks create-addon --cluster-name my-cluster --addon-name eks-pod-identity-agent
aws eks create-pod-identity-association --cluster-name my-cluster --namespace default \
  --service-account files --role-arn arn:aws:iam::123456789012:role/files

kubectl apply -f kubernetes.yaml
