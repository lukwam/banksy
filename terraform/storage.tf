resource "google_storage_bucket" "confirmed" {
  name                        = "${google_project.project.project_id}-confirmed"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "incoming" {
  name                        = "${google_project.project.project_id}-incoming"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "notbanksy" {
  name                        = "${google_project.project.project_id}-notbanksy"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "official" {
  name                        = "${google_project.project.project_id}-official"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}
