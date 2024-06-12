terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.32.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = var.project
  region  = var.region
  credentials = file(var.credentials)
}
# Resource: Google Storage Bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

# Resource:
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  location = var.location

}