# SRE Automation Demo Presentation

This document presents the project narrative, architecture, demo flow, and key engineering decisions.

## 1. Opening Story

This demo shows how I would automate deployment of a containerized microservice onto cloud infrastructure. Terraform owns infrastructure state. Python owns workflow orchestration, validation, deployment safety, rollback, observability, and CI/CD integration. Ansible handles host configuration and application runtime setup for the EC2 path.

## 2. Architecture Sketch

```text
PR -> CI -> container build -> Terraform plan -> approval -> deploy
                                                 |
                                                 +-> EC2 provisioning
                                                 +-> Ansible Docker setup
                                                 +-> container rollout
                                                 +-> smoke checks
                                                 +-> health/SLO validation
                                                 +-> logs/metrics
```

Key points:

- Build once, promote the same immutable artifact through dev, staging, and prod.
- Use environment-specific config and secret references, not environment-specific code.
- Keep Terraform modules reusable and state isolated per environment.
- Make production changes auditable through pull requests, plans, approvals, and deployment records.
- Use Ansible for repeatable host configuration when deploying to VM-based infrastructure.

## 3. Code Walkthrough

Start with:

```bash
tree -a -I '.venv|.git|__pycache__|.pytest_cache|.ruff_cache'
```

Show:

- `src/sre_automation/cli.py`: clean command interface.
- `src/sre_automation/config.py`: typed config loading.
- `src/sre_automation/deploy.py`: orchestration flow.
- `src/sre_automation/terraform.py`: subprocess wrapper with retries and metrics.
- `src/sre_automation/secrets.py`: validates secret references without exposing values.
- `examples/config/*.yaml`: environment promotion model.
- `.github/workflows/ci.yml`: CI/CD gates and deployment approval.
- `app/main.py`: small FastAPI service with health, readiness, metrics, and sample API endpoints.
- `app/Dockerfile`: container packaging for the application.
- `terraform/modules/ec2_app`: AWS EC2 infrastructure module.
- `ansible/playbooks/deploy_app.yml`: host configuration and container rollout.

## 4. Demo Commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

Dry-run plan:

```bash
sre-deploy plan --config examples/config/dev.yaml --image-tag sha-demo123 --dry-run
```

Dry-run deployment:

```bash
sre-deploy deploy \
  --config examples/config/prod.yaml \
  --image-tag sha-demo123 \
  --previous-image-tag sha-previous \
  --dry-run
```

Container build:

```bash
docker build -t orders-api:local app
docker run --rm -p 8080:8080 orders-api:local
```

EC2 provisioning path:

```bash
cd terraform/envs/aws-dev
terraform init
terraform plan \
  -var="ami_id=ami-0123456789abcdef0" \
  -var="key_name=my-ec2-keypair" \
  -var='ssh_cidr_blocks=["203.0.113.10/32"]'
```

Point out the structured JSON events in stdout. In production, these would be shipped to OpenSearch/Loki and converted to metrics through OpenTelemetry or a collector.

## 5. CI/CD Explanation

The workflow has four layers:

- Python job: install, lint, unit test.
- Container job: build the FastAPI image and push to GHCR outside pull requests.
- Terraform job: format, init without backend, validate local and EC2 environments.
- Deploy jobs: dry-run orchestrator or real EC2 provisioning plus Ansible deployment.

For production I would add:

- Terraform plan artifact attached to PR.
- OIDC-based cloud auth instead of static credentials.
- Checkov/tfsec policy scans.
- SBOM and container scanning.
- Deployment freeze windows and change-ticket integration if required.

## 6. Secrets And Promotion

The YAML files hold references only:

```yaml
secret_refs:
  db_password: aws-secretsmanager://prod/orders-api/db_password
  api_token: vault://kv/prod/orders-api/api_token
```

Talking point:

Secrets are resolved at runtime by workload identity or cloud IAM. They are never committed, printed, or passed through CI logs.

## 7. Observability

This demo emits structured events:

- `deployment_started`
- `command_started`
- `metric`
- `smoke_check_completed`
- `service_health_validated`
- `deployment_completed`
- `rollback_started`

Production design:

- Metrics: Prometheus/OpenTelemetry.
- Logs: JSON to OpenSearch, Elasticsearch, or Loki.
- Traces: OpenTelemetry spans around deploy phases.
- Alerts: error budget burn, failed deployments, rollback failures, elevated service error rate.

## 8. Rollback Discussion

Rollback should be boring and explicit:

- Track previous artifact.
- Revert to previous known-good artifact.
- Re-run smoke checks.
- Emit rollback telemetry.
- Create incident or change record if production was impacted.

## 9. Generative AI For SRE

Recommended uses:

- Incident summarization.
- Runbook search.
- Alert explanation.
- Postmortem draft generation.
- Test-case generation for automation scripts.
- Read-only ChatOps assistant for recent deploys, logs, and dashboards.

Guardrails:

- Read-only by default.
- Human approval for destructive actions.
- RBAC and audit logs.
- No secrets in prompts.
- Retrieval from trusted internal docs.
- Generated code still goes through tests, scans, and review.

## 10. Insider Risk Evaluation

Definition:

Insider risk is the potential for harm caused by trusted users or compromised trusted accounts misusing or mishandling authorized access.

Evaluation criteria for an insider-risk platform:

- Detection quality for malicious, negligent, and compromised-user behavior.
- Peer-group anomaly detection and behavioral baselining.
- Explainable risk scoring.
- Low false positives.
- Endpoint, cloud, server, SaaS, and privileged-account coverage.
- Privacy controls, investigator audit logs, and role-based access.
- SIEM/SOAR/ticketing integrations.
- Enterprise scale and endpoint performance.

Example evaluation scenarios:

- Unusual file access before resignation.
- Sensitive upload to personal cloud storage.
- Privileged account activity outside normal behavior.
- Attempted bypass of monitoring controls.
- Abnormal access from unusual location.

## 11. Strong Closing

The theme is not “Python versus Terraform.” The theme is using each tool at the right layer: Terraform manages desired state; Python coordinates safe operational workflows around it.
