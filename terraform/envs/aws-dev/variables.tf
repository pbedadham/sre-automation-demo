variable "environment" {
  type    = string
  default = "dev"
}

variable "region" {
  type    = string
  default = "us-west-2"
}

variable "service_name" {
  type    = string
  default = "orders-api"
}

variable "ami_id" {
  description = "Amazon Linux 2023 AMI ID for the selected region."
  type        = string
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "key_name" {
  type    = string
  default = null
}

variable "ssh_cidr_blocks" {
  type    = list(string)
  default = []
}

variable "app_port" {
  type    = number
  default = 8080
}

variable "root_volume_size" {
  type    = number
  default = 20
}

variable "tags" {
  type = map(string)
  default = {
    Project   = "sre-automation-demo"
    ManagedBy = "terraform"
  }
}
