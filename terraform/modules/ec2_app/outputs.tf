output "instance_id" {
  description = "EC2 instance ID."
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "EC2 public IP address."
  value       = aws_instance.app.public_ip
}

output "public_dns" {
  description = "EC2 public DNS name."
  value       = aws_instance.app.public_dns
}

output "security_group_id" {
  description = "Application security group ID."
  value       = aws_security_group.app.id
}

output "application_url" {
  description = "Application health URL."
  value       = "http://${aws_instance.app.public_dns}:${var.app_port}/health"
}
