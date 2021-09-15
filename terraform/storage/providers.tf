provider "google" {
  version = "3.38.0"

  credentials = file("terraform_account.json")

  project = var.project_id
  region  = var.region
  zone    = var.zone
}