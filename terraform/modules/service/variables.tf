variable "environment" {
  description = "Deployment environment name."
  type        = string
}

variable "region" {
  description = "Cloud region."
  type        = string
}

variable "service_name" {
  description = "Service name."
  type        = string
}

variable "service_port" {
  description = "Service port."
  type        = string
}

variable "image_tag" {
  description = "Immutable image or artifact tag."
  type        = string
}
