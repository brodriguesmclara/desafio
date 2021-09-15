variable "project_id" {
  description = "Project where the dataset and table are created."
  type = string
  default = "local-terminus-325600"
}

variable "location" {
  description = "location dataset."
  type = string
  default = "us-central1"
}

variable "expiration_ms" {
  description = "Número de milissegundos para os quais manter o armazenamento de uma partição."
  type = number
  default = null
}

variable "expiration_time" {
  description = "A hora em que esta tabela expira, em milissegundos. "
  type = string
  default = null
}

variable "require_partition_filter" {
  description = "Se definido como verdadeiro, as consultas sobre esta tabela requerem a especificação de um filtro de partição que pode ser usado para eliminação da partição."
  type = bool
  default = false
}

variable "time_partitioning" {
  description = "type partitioning."
  type = string
  default = ""
}

variable "field_partitioning" {
  description = "field partitioning."
  type = string
  default = ""
}

variable "dataset_name" {
  description = "dataset name"
  type = string
  default = "dasa_bi"
}

variable "dataset_id" {
  description = "dataset id"
  type = string
  default = "dasa_bi"
}

variable "region" {
  description = "region do project."
  type = string
  default = "us-central1"
}

variable "zone" {
  description = "zone do project."
  type = string
  default = "us-central1-a"
}

variable "delete_contents_on_destroy" {
  description = "(Optional) If set to true, delete all the tables in the dataset when destroying the resource; otherwise, destroying the resource will fail if tables are present."
  type        = bool
  default     = null
}