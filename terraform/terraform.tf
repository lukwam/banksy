terraform {
  backend "gcs" {
    bucket = "lukwam-banksy-tf"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.82.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "3.82.0"
    }
  }
}
