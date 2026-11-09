# The image of the application, with its pre-forking server and Pyjo-AWS of the script
uv run app.py generate dockerfile
docker build --platform linux/arm64 -t 123456789012.dkr.ecr.eu-central-1.amazonaws.com/jobs:1.0 .
docker push 123456789012.dkr.ecr.eu-central-1.amazonaws.com/jobs:1.0

# The task, whose role gives the credentials of the application, and its service, which replaces the tasks one by one
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs update-service --cluster my-cluster --service jobs --task-definition jobs
