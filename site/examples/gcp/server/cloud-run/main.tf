# The equivalent of gcloud run services replace of deploy.sh, for OpenTofu or Terraform; the image stays in deploy.sh

terraform {
  required_version = ">= 1.10"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }
}

provider "google" {
  project = "myproject"
  region  = "europe-west1"
}

resource "google_cloud_run_v2_service" "myapp" {
  name     = "myapp"
  location = "europe-west1"

  template {
    # The service account of the token of the metadata server, with the role Storage Object Viewer on the bucket
    service_account = "myapp-sa@myproject.iam.gserviceaccount.com"

    containers {
      image = "europe-west1-docker.pkg.dev/myproject/apps/myapp"

      env {
        name  = "BUCKET"
        value = "mybucket"
      }

      # The log of JSON, which Cloud Logging reads with its levels
      env {
        name  = "PYJO_LOG_FORMAT"
        value = "json"
      }

      startup_probe {
        http_get {
          path = "/readyz"
        }
      }

      liveness_probe {
        http_get {
          path = "/livez"
        }
      }
    }
  }
}
