variable "project_id" {
  description = "Project ID where Cloud Composer Environment is created."
  type        = string
  default = "local-terminus-325600"
}

variable "composer_env_name" {
  description = "Name of Cloud Composer Environment"
  type        = string
  default = "dasa-orchestrator"
}

variable region {
  default = "us-east1"
}

variable zone {
  default     = "us-east1-b"
}

variable "node_count" {
  description = "Number of worker nodes in Cloud Composer Environment."
  type        = number
  default     = 3
}

variable "machine_type" {
  description = "Machine type of Cloud Composer nodes."
  type        = string
  default     = "n1-standard-1"
}

variable "disk_size_gb" {
  type = number
  default = 20
}

