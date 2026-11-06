terraform {
  # use_lockfile of the backend s3
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 3.0"
    }
  }

  # The bucket of the state of Pyjoyment-Lambda-Layers, of the same account, with a key of its own
  backend "s3" {
    bucket       = "pyjoyment-tofu-state-959435416781"
    key          = "pyjoyment.dev/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}

# us-east-1 for everything, as CloudFront takes its certificate from there only
provider "aws" {
  region = "us-east-1"

  # The credentials come from AWS_PROFILE, and a profile of another account fails before it changes anything
  allowed_account_ids = [local.account_id]

  default_tags {
    tags = {
      Repository = local.repository
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

locals {
  account_id = "959435416781"
  repository = "pyjoyment/pyjoyment.dev"
  domain     = "pyjoyment.dev"
  name       = "pyjoyment-dev"
}
