module "bigquery" {
  source  = "terraform-google-modules/bigquery/google"
  version = "~> 4.3"  
  
  dataset_id                 = var.dataset_id
  dataset_name               = var.dataset_name 
  project_id                 = var.project_id
  location                   = var.location
  delete_contents_on_destroy = var.delete_contents_on_destroy
  
}


  
