# The equivalent of instance.sh, for OpenTofu or Terraform, with the steps on the instance in its startup script

terraform {
  required_version = ">= 1.11"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
}

provider "google" {
  project = "myproject"
}

# A service account of the instance, which reads the secret, and the secret itself, written only, so that the state
# does not keep it
resource "google_service_account" "myapp" {
  account_id = "myapp-sa"
}

resource "google_secret_manager_secret" "session" {
  secret_id = "myapp-session"

  replication {
    auto {}
  }
}

ephemeral "random_password" "session" {
  length = 32
}

resource "google_secret_manager_secret_version" "session" {
  secret                 = google_secret_manager_secret.session.id
  secret_data_wo         = ephemeral.random_password.session.result
  secret_data_wo_version = 1
}

resource "google_secret_manager_secret_iam_member" "session" {
  secret_id = google_secret_manager_secret.session.id
  role      = "roles/secretmanager.secretAccessor"
  member    = google_service_account.myapp.member
}

# The instance, whose metadata server gives the token of the service account of the scope of all the APIs, which its
# roles limit, and app.py and its unit as attributes of its metadata, which its startup script reads on each boot
resource "google_compute_instance" "myapp" {
  name         = "myapp-1"
  zone         = "europe-west1-b"
  machine_type = "e2-small"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = "default"
  }

  service_account {
    email  = google_service_account.myapp.email
    scopes = ["cloud-platform"]
  }

  metadata = {
    app-py         = file("app.py")
    myapp-service  = file("myapp.service")
    startup-script = <<-EOT
      #!/bin/sh
      attribute() { curl -fsS -H Metadata-Flavor:Google "http://metadata.google.internal/computeMetadata/v1/instance/attributes/$1"; }
      id myapp || useradd --system myapp
      command -v uv || curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
      mkdir -p /opt/myapp && attribute app-py > /opt/myapp/app.py
      uv venv --allow-existing /opt/myapp/.venv && uv pip install --python /opt/myapp/.venv Pyjoyment Pyjo-GCP
      attribute myapp-service > /etc/systemd/system/myapp.service
      systemctl daemon-reload && systemctl enable --now myapp
    EOT
  }
}
