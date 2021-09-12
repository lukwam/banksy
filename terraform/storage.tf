resource "google_storage_bucket" "confirmed" {
  name                        = "${var.project_id}-confirmed"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "incoming" {
  name                        = "${var.project_id}-incoming"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "notbanksy" {
  name                        = "${var.project_id}-notbanksy"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}
