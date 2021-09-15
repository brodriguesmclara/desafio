module "gcs_buckets" {
  source  = "terraform-google-modules/cloud-storage/google"
  version = "~> 1.7"
  project_id  = var.project_id
  names = var.name
  prefix = var.prefix
  location = var.location
  storage_class = var.storage_class
  folders = var.folders
}