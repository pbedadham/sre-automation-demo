resource "null_resource" "service_release" {
  triggers = {
    environment  = var.environment
    region       = var.region
    service_name = var.service_name
    service_port = var.service_port
    image_tag    = var.image_tag
  }
}
