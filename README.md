# SRE Automation Demo

This repository presents a Python-driven SRE automation project. It shows how Python can orchestrate safe infrastructure deployment workflows while Terraform remains the declarative source of truth for cloud resources.

## What This Demonstrates

- Python-driven SRE automation for provisioning and deployment workflows
- Terraform module and environment layout for dev, staging, and prod
- CI/CD gates for linting, testing, Terraform planning, and production approval
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
Cloud infrastructure + Kubernetes/ECS/VMs
   |
   v
Prometheus/Grafana/OpenSearch/Alertmanager
```

## Repository Layout

```text
.
├── .github/workflows/ci.yml
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
│   ├── modules/service/
│   └── envs/
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

## Presentation Guide

[docs/presentation.md](docs/presentation.md) provides the project narrative, architecture diagrams, demo commands, and key technical points.

## Important Note

The Terraform code intentionally uses `null_resource` and local commands so the demo can run without cloud credentials. In a real AWS or GCP implementation, the same module boundaries would provision cloud networking, compute, IAM, secrets integration, and observability resources.
