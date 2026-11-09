# The equivalent of the commands of gcloud of iam.sh, for OpenTofu or Terraform; the image and kubectl stay in iam.sh

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
}

variable "federation" {
  description = "Workload Identity Federation for GKE, without a service account of Google nor the annotation"
  type        = bool
  default     = false
}

# A service account of Google that publishes to the topic, which the service account of Kubernetes of the annotation
# acts as
resource "google_service_account" "publisher" {
  count      = var.federation ? 0 : 1
  account_id = "publisher"
}

resource "google_pubsub_topic_iam_member" "publisher" {
  count  = var.federation ? 0 : 1
  topic  = "events"
  role   = "roles/pubsub.publisher"
  member = google_service_account.publisher[0].member
}

resource "google_service_account_iam_member" "workload_identity" {
  count              = var.federation ? 0 : 1
  service_account_id = google_service_account.publisher[0].name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:myproject.svc.id.goog[default/myapp]"
}

# Or the role of the principal of the service account of Kubernetes, of the number of the project
resource "google_pubsub_topic_iam_member" "federation" {
  count  = var.federation ? 1 : 0
  topic  = "events"
  role   = "roles/pubsub.publisher"
  member = "principal://iam.googleapis.com/projects/123456789012/locations/global/workloadIdentityPools/myproject.svc.id.goog/subject/ns/default/sa/myapp"
}
