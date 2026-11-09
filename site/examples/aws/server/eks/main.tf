# The equivalent of the commands of aws of deploy.sh, for OpenTofu or Terraform; docker and kubectl stay in deploy.sh

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

# EKS Pod Identity, instead of the annotation of IRSA: its agent, and the role of the service account
resource "aws_eks_addon" "pod_identity" {
  cluster_name = "my-cluster"
  addon_name   = "eks-pod-identity-agent"
}

resource "aws_eks_pod_identity_association" "files" {
  cluster_name    = "my-cluster"
  namespace       = "default"
  service_account = "files"
  role_arn        = "arn:aws:iam::123456789012:role/files"
}
