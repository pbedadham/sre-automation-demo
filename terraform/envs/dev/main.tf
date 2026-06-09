terraform {
  required_version = ">= 1.6.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }

  # Real environments should use remote state with locking, for example S3+DynamoDB
  # or Terraform Cloud. Local state is used here so the demo is self-contained.
}

module "service" {
  source = "../../modules/service"

  environment  = var.environment
  region       = var.region
  service_name = var.service_name
  service_port = var.service_port
  image_tag    = var.image_tag
}
