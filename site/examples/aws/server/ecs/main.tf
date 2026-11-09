# The equivalent of the commands of aws of deploy.sh, for OpenTofu or Terraform; the image stays in deploy.sh

terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

# The task of task-definition.json, whose role gives the credentials of the application
locals {
  task = jsondecode(file("task-definition.json"))
}

resource "aws_ecs_task_definition" "jobs" {
  family                   = local.task.family
  task_role_arn            = local.task.taskRoleArn
  execution_role_arn       = local.task.executionRoleArn
  network_mode             = local.task.networkMode
  requires_compatibilities = local.task.requiresCompatibilities
  cpu                      = local.task.cpu
  memory                   = local.task.memory
  container_definitions    = jsonencode(local.task.containerDefinitions)

  runtime_platform {
    cpu_architecture        = local.task.runtimePlatform.cpuArchitecture
    operating_system_family = local.task.runtimePlatform.operatingSystemFamily
  }
}

# The service, which replaces its tasks one by one with the ones of a new revision of the task
resource "aws_ecs_service" "jobs" {
  name            = "jobs"
  cluster         = "my-cluster"
  task_definition = aws_ecs_task_definition.jobs.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = ["subnet-0123456789abcdef0", "subnet-0123456789abcdef1"]
    security_groups = ["sg-0123456789abcdef0"]
  }
}
