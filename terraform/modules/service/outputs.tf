output "release_id" {
  description = "Synthetic release identifier for the demo."
  value       = "${var.environment}-${var.service_name}-${var.image_tag}"
}
