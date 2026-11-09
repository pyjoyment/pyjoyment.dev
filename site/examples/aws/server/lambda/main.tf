# The equivalent of the commands of aws of deploy.sh, for OpenTofu or Terraform: tofu apply after generate lambda-zip

terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

# The public layer of the Pyjoyment of the ZIP, of the runtime and the region of the function
data "http" "layers" {
  url = "https://github.com/pyjoyment/Pyjoyment-Lambda-Layers/releases/latest/download/layers.json"
}

# The ZIP of generate lambda-zip --function-only, whose code a plan compares by its hash
resource "aws_lambda_function" "notes" {
  function_name    = "notes"
  runtime          = "python3.15"
  architectures    = ["arm64"]
  handler          = "app.handler"
  filename         = "dist/function.zip"
  source_code_hash = filebase64sha256("dist/function.zip")
  layers           = [jsondecode(data.http.layers.response_body)["pyjoyment-0_3_0-python3_15"]["eu-central-1"]]
  role             = "arn:aws:iam::123456789012:role/notes"

  environment {
    variables = {
      TABLE = "notes"
    }
  }
}

resource "aws_lambda_function_url" "notes" {
  function_name      = aws_lambda_function.notes.function_name
  authorization_type = "AWS_IAM"
}
