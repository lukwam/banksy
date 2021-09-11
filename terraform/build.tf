resource "google_cloudbuild_trigger" "deploy-process-incoming-images-function" {
  provider       = google-beta
  name           = "deploy-process-incoming-images-function"
  description    = "Deploy process_incoming_images Function"
  filename       = "functions/process_incoming_images/cloudbuild.yaml"
  project        = var.project_id

  github {
    name     = "banksy"
    owner    = "lukwam"
    push {
      branch = "^main$"
    }
  }

  included_files = [
    "functions/process_incoming_images/**",
  ]

  ignored_files = [
    "functions/process_incoming_images/*.md",
    "functions/process_incoming_images/*.sh",
  ]

  substitutions = {
    _INCOMING_BUCKET = "${var.project_id}-incoming"
  }

  depends_on = [
    google_project_service.services["cloudbuild.googleapis.com"]
  ]
}
