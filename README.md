# SRE Automation Demo

This repository presents a Python-driven SRE automation project. It shows how Python can orchestrate safe infrastructure deployment workflows while Terraform remains the declarative source of truth for cloud resources.

## What This Demonstrates

- Python-driven SRE automation for provisioning and deployment workflows
- Terraform module and environment layout for dev, staging, and prod
- Real AWS EC2 provisioning example for a containerized FastAPI service
- Ansible configuration management to install Docker and run the service
- CI/CD gates for linting, testing, Terraform planning, and production approval
- GitHub Actions build, push, provision, and deploy flow
- Secret and configuration handling patterns
- Observability hooks for deployment logs, metrics, health checks, and rollback
- Generative AI recommendations for SRE productivity
- Insider-risk evaluation criteria for enterprise security platforms

## Architecture

```text
Developer PR
   |
   v
GitHub Actions
   |
   +-- Python lint/test
   +-- Docker build/push to Docker Hub
   +-- Terraform fmt/validate/plan
   +-- security scanning placeholder
   |
   v
Environment approval gate
   |
   v
Python deployment orchestrator
   |
   +-- load environment config
   +-- resolve secret references
   +-- run Terraform init/plan/apply
   +-- deploy immutable service artifact
   +-- run smoke checks
   +-- emit logs/metrics
   +-- rollback on failure
   |
   v
EC2 + Docker + FastAPI service
   |
   v
Prometheus/Grafana/OpenSearch/Alertmanager
```

## Repository Layout

```text
.
├── .github/workflows/ci.yml
├── ansible/
│   ├── ansible.cfg
│   ├── inventory.ini.example
│   └── playbooks/deploy_app.yml
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── docs/
│   ├── presentation.md
│   ├── observability.md
│   ├── generative-ai-for-sre.md
│   └── insider-risk-evaluation.md
├── examples/config/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── prod.yaml
├── src/sre_automation/
│   ├── cli.py
│   ├── config.py
│   ├── deploy.py
│   ├── observability.py
│   ├── rollback.py
│   ├── secrets.py
│   └── terraform.py
├── terraform/
│   ├── modules/
│   │   ├── ec2_app/
│   │   └── service/
│   └── envs/
│       ├── aws-dev/
│       ├── dev/
│       ├── staging/
│       └── prod/
└── tests/
```

## Quick Start

Create a virtual environment and run tests:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run a dry-run deployment:

```bash
sre-deploy deploy \
  --config examples/config/dev.yaml \
  --image-tag sha-demo123 \
  --dry-run
```

Run a plan-only Terraform orchestration:

```bash
sre-deploy plan \
  --config examples/config/staging.yaml \
  --image-tag sha-demo123 \
  --dry-run
```

Run the FastAPI app locally:

```bash
cd app
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

Build the application container locally:

```bash
docker build -t orders-api:local app
docker run --rm -p 8080:8080 orders-api:local
```

## EC2 Deployment Path

The `terraform/envs/aws-dev` environment provisions:

- EC2 instance
- security group for application traffic and optional SSH
- IAM role and instance profile with SSM access
- encrypted root EBS volume
- outputs for public IP, DNS, and application health URL

The Ansible playbook then:

- installs Docker
- logs in to Docker Hub when credentials are provided
- pulls the application image
- runs the FastAPI container
- validates `/health`

For a real GitHub Actions deployment with `deploy_target=aws-ec2`, configure these repository secrets:

- `AWS_ROLE_TO_ASSUME`: IAM role used by GitHub OIDC
- `EC2_SSH_PRIVATE_KEY`: private key matching the EC2 key pair
- `DOCKERHUB_USERNAME`: Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token

Regular pull requests and pushes build the image without pushing it. Set the optional repository variable `DOCKERHUB_REPOSITORY` if the image should be pushed somewhere other than `pbedadham/sre-automation-demo`. Then run the workflow manually with `deploy_target=aws-ec2`, an Amazon Linux 2023 `ami_id`, `key_name`, and an SSH CIDR allowlist.

## Presentation Guide

[docs/presentation.md](docs/presentation.md) provides the project narrative, architecture diagrams, demo commands, and key technical points.

## Important Note

The default Terraform environments use `null_resource` so the core demo can run without cloud credentials. The `aws-dev` environment shows the real EC2 path for provisioning infrastructure and deploying the containerized application.
