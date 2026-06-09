variable "environment" {
  description = "Deployment environment name."
  type        = string
}

variable "region" {
  description = "AWS region."
  type        = string
}

variable "service_name" {
  description = "Application service name."
  type        = string
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance. Use an Amazon Linux 2023 AMI."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Optional EC2 key pair name for SSH access."
  type        = string
  default     = null
}

variable "ssh_cidr_blocks" {
  description = "CIDR blocks allowed to reach SSH."
  type        = list(string)
  default     = []
}

variable "app_port" {
  description = "Application container port."
  type        = number
  default     = 8080
}

variable "root_volume_size" {
  description = "Root EBS volume size in GiB."
  type        = number
  default     = 20
}

variable "tags" {
  description = "Additional AWS tags."
  type        = map(string)
  default     = {}
}
