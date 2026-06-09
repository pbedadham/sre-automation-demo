output "instance_id" {
  value = module.ec2_app.instance_id
}

output "public_ip" {
  value = module.ec2_app.public_ip
}

output "public_dns" {
  value = module.ec2_app.public_dns
}

output "application_url" {
  value = module.ec2_app.application_url
}
