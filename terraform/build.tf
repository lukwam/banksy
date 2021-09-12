resource "google_cloudbuild_trigger" "deploy-app" {
  provider       = google-beta
  name           = "deploy-app"
  description    = "Deploy App"
  filename       = "app/cloudbuild.yaml"
  project        = var.project_id

  github {
    name     = "banksy"
    owner    = "lukwam"
    push {
      branch = "^main$"
    }
  }

  included_files = [
    "app/**",
  ]

  ignored_files = [
    "app/*.md",
    "app/*.sh",
  ]

  depends_on = [
    google_project_service.services["cloudbuild.googleapis.com"]
  ]
}



resource "google_cloudbuild_trigger" "deploy-process-incoming-image-function" {
  provider       = google-beta
  name           = "deploy-process-incoming-image-function"
  description    = "Deploy process_incoming_image Function"
  filename       = "functions/process_incoming_image/cloudbuild.yaml"
  project        = var.project_id

  github {
    name     = "banksy"
    owner    = "lukwam"
    push {
      branch = "^main$"
    }
  }

  included_files = [
    "functions/process_incoming_image/**",
  ]

  ignored_files = [
    "functions/process_incoming_image/*.md",
    "functions/process_incoming_image/*.sh",
  ]

  substitutions = {
    _INCOMING_BUCKET = "${var.project_id}-incoming"
  }

  depends_on = [
    google_project_service.services["cloudbuild.googleapis.com"]
  ]
}
