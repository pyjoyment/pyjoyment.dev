# The equivalent of deploy.sh, for OpenTofu or Terraform, with the instance itself, which deploy.sh takes as it is

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

data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64"
}

# The instance profile of the role of the application, and IMDSv2 only, whose token Pyjo-AWS takes; cloud-init puts
# app.py and its unit on the instance, with Pyjo-AWS of the script in a virtual environment, as deploy.sh does by hand
resource "aws_instance" "myapp" {
  ami                  = data.aws_ssm_parameter.al2023.value
  instance_type        = "t4g.small"
  iam_instance_profile = "myapp"

  metadata_options {
    http_tokens = "required"
  }

  user_data = <<-EOT
    #cloud-config
    users:
      - name: myapp
        system: true
    write_files:
      - path: /opt/myapp/app.py
        encoding: b64
        content: ${filebase64("app.py")}
      - path: /etc/systemd/system/myapp.service
        encoding: b64
        content: ${filebase64("myapp.service")}
    runcmd:
      - curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
      - cd /opt/myapp && uv venv && VIRTUAL_ENV=/opt/myapp/.venv uv sync --script app.py --active
      - systemctl daemon-reload
      - systemctl enable --now myapp
  EOT
}
