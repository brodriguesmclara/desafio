variable "project_id" {
  description = "Bucket project id."
  type        = string
  default    = "local-terminus-325600"
}

variable "region" {
  description = "Bucket region"
  type        = string
  default    = "us-central1"
}

variable "zone" {
  description = "Bucket zone"
  type        = string
  default    = "us-central1-a"
}

variable "location" {
  description = "Bucket location"
  type        = string
  default    = "us-central1"
}

variable "storage_class" {
  description = "Bucket storage class"
  type        = string
  default    = "Standard"
}

variable "prefix" {
  description = "Bucket prefix"
  type        = string
  default    = ""
}

variable "name" {
  description = "Bucket name"
  type        = list
  default    = ["dasa-saude"]
}

variable "folders" {
  description = "Bucket folders"
  type        = map
  default    = {
    dasa-saude = ["input_file",
                  "output_file",
                  "codigos",
                        ]
  }
}

