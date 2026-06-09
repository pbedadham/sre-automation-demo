terraform {
  required_version = ">= 1.6.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }

  # Example production backend:
  # backend "s3" {
  #   bucket         = "org-terraform-state-prod"
  #   key            = "orders-api/prod.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "terraform-locks"
  #   encrypt        = true
  # }
}

module "service" {
  source = "../../modules/service"

  environment  = var.environment
  region       = var.region
  service_name = var.service_name
  service_port = var.service_port
  image_tag    = var.image_tag
}
