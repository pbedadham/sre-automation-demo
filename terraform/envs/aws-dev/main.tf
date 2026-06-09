terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Example backend for a real shared environment:
  # backend "s3" {
  #   bucket         = "org-terraform-state-dev"
  #   key            = "orders-api/aws-dev.tfstate"
  #   region         = "us-west-2"
  #   dynamodb_table = "terraform-locks"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.region
}

module "ec2_app" {
  source = "../../modules/ec2_app"

  environment      = var.environment
  region           = var.region
  service_name     = var.service_name
  ami_id           = var.ami_id
  instance_type    = var.instance_type
  key_name         = var.key_name
  ssh_cidr_blocks  = var.ssh_cidr_blocks
  app_port         = var.app_port
  root_volume_size = var.root_volume_size
  tags             = var.tags
}
