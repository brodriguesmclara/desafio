resource "google_composer_environment" "composer_env" {
       name    = var.composer_env_name
       project = var.project_id
       region  = var.region

      config {
           node_count     = var.node_count

           node_config {
               zone                 = var.zone
               disk_size_gb         = var.disk_size_gb
               service_account      = null
            }
        }
    }
      


