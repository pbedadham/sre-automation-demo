# SRE Automation Demo Presentation

This is the narrative I use to explain the project, the architecture, and the main engineering decisions.

## 1. Project Overview

I built this as a practical SRE automation example for deploying a containerized Python service onto cloud infrastructure. The design separates responsibilities clearly:

- Terraform manages infrastructure state.
- Python coordinates deployment workflow, validation, retries, logging, metrics, and rollback.
- Ansible configures the EC2 host and runs the application container.
- Docker packages the FastAPI service.
- GitHub Actions connects code changes to build, validation, and deployment.

The main idea is that infrastructure automation should be repeatable, observable, and safe to promote across environments.

## 2. Architecture

```mermaid
flowchart LR
    Dev[Developer PR or Push] --> GA[GitHub Actions]

    GA --> Test[Python Tests and Ruff]
    GA --> Build[Build Docker Image]
    Build --> GHCR[GitHub Container Registry]
    GA --> TFCheck[Terraform fmt and validate]

    GA --> Gate[Environment Approval]
    Gate --> Choice{Deploy Target}

    Choice --> DryRun[Python Orchestrator Dry Run]
    Choice --> EC2Path[Terraform Apply aws-dev]

    EC2Path --> AWS[(AWS)]
    AWS --> EC2[EC2 Instance]
    EC2Path --> Outputs[Public IP and App URL]
    Outputs --> Ansible[Ansible Playbook]
    GHCR --> Ansible
    Ansible --> Docker[Docker on EC2]
    Docker --> App[FastAPI Orders API]

    App --> Health[/health and /ready]
    App --> Metrics[/metrics]
    DryRun --> Events[Structured Logs and Metrics]
    Health --> Events
    Metrics --> Obs[Prometheus, Grafana, OpenSearch]
```

The artifact flow is intentionally simple: build the image once, tag it immutably, and promote that same image through environments. Environment differences live in config, Terraform variables, and secret references.

## 3. Codebase Structure

The repo is organized around ownership boundaries:

- `app/`: the FastAPI service and Dockerfile.
- `src/sre_automation/`: the Python automation package.
- `terraform/modules/`: reusable infrastructure modules.
- `terraform/envs/`: environment-specific Terraform roots.
- `ansible/`: host configuration and application rollout.
- `.github/workflows/ci.yml`: CI/CD workflow.
- `examples/config/`: environment config for the Python orchestrator.
- `docs/`: supporting material for observability, GenAI, and insider risk.

Files I focus on during the walkthrough:

- `src/sre_automation/cli.py`: command entry point.
- `src/sre_automation/deploy.py`: deployment orchestration flow.
- `src/sre_automation/terraform.py`: Terraform wrapper with retries and timing metrics.
- `src/sre_automation/secrets.py`: secret reference validation.
- `app/main.py`: FastAPI app with health, readiness, metrics, and sample API endpoints.
- `terraform/modules/ec2_app/main.tf`: EC2, security group, IAM, and root volume.
- `ansible/playbooks/deploy_app.yml`: Docker install, image pull, container run, and health check.

## 4. Python-Driven SRE Automation

The Python layer is responsible for operational workflow, not for replacing Terraform.

In this project, Python:

- loads typed environment config
- validates secret references
- runs Terraform `init`, `plan`, and `apply`
- supports dry-run execution
- emits structured deployment events
- measures command and deployment duration
- runs smoke and health checks
- calls rollback logic when deployment fails

The deployment path is:

```text
sre-deploy deploy
  -> load YAML config
  -> validate secret references
  -> terraform init/plan/apply
  -> roll out artifact
  -> smoke check
  -> health validation
  -> rollback on failure
```

I keep Terraform as the source of truth for desired infrastructure state. Python gives me the control plane around that state: safety checks, promotion rules, observability, and rollback behavior.

## 5. Demo Commands

Run the local verification:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pip install -r app/requirements.txt
pytest
ruff check .
```

Run a safe dry-run plan:

```bash
sre-deploy plan --config examples/config/dev.yaml --image-tag sha-demo123 --dry-run
```

Run a safe dry-run deployment:

```bash
sre-deploy deploy \
  --config examples/config/prod.yaml \
  --image-tag sha-demo123 \
  --previous-image-tag sha-previous \
  --dry-run
```

Build and run the application container:

```bash
docker build -t orders-api:local app
docker run --rm -p 8080:8080 orders-api:local
curl http://127.0.0.1:8080/health
```

Review the EC2 provisioning path:

```bash
cd terraform/envs/aws-dev
terraform init
terraform plan \
  -var="ami_id=ami-0123456789abcdef0" \
  -var="key_name=my-ec2-keypair" \
  -var='ssh_cidr_blocks=["203.0.113.10/32"]'
```

## 6. CI/CD Flow

The GitHub Actions workflow has four main parts:

- `python`: installs dependencies, runs linting, and runs tests.
- `container`: builds the FastAPI Docker image and pushes it to GHCR when deployment needs a published artifact.
- `terraform`: validates both the safe local Terraform environment and the AWS EC2 environment.
- `deploy-dry-run` / `deploy-aws-ec2`: either runs the Python orchestrator safely or provisions EC2 and deploys the container with Ansible.

For the real EC2 path, the workflow expects:

- `AWS_ROLE_TO_ASSUME`: IAM role for GitHub OIDC.
- `EC2_SSH_PRIVATE_KEY`: SSH key used by Ansible.
- workflow inputs for `ami_id`, `key_name`, region, instance type, and SSH CIDR allowlist.

In a production version, I would also add Terraform plan artifacts, policy checks, SBOM generation, image vulnerability scanning, and stricter environment approval rules.

## 7. Secrets, Config, And Promotion

The environment YAML files contain secret references, not secret values:

```yaml
secret_refs:
  db_password: aws-secretsmanager://prod/orders-api/db_password
  api_token: vault://kv/prod/orders-api/api_token
```

The promotion model is:

```text
dev -> staging -> prod
same image tag, different environment config
```

That keeps the artifact immutable. The service is not rebuilt for each environment; only the runtime configuration and infrastructure variables change.

## 8. Observability And Error Handling

The automation emits structured events such as:

- `deployment_started`
- `command_started`
- `metric`
- `smoke_check_completed`
- `service_health_validated`
- `deployment_completed`
- `rollback_started`

The application also exposes:

- `/health`
- `/ready`
- `/metrics`

In production, I would ship deployment logs to OpenSearch or Loki, scrape service metrics with Prometheus or OpenTelemetry, and build dashboards in Grafana. Alerts should focus on user impact: failed deployments, rollback failures, elevated 5xx rate, latency SLO violations, queue age, and error-budget burn.

## 9. Rollback

Rollback is modeled as an explicit deployment phase. The automation records the previous image tag, attempts to restore it on failure, emits rollback events, and would re-run health checks after restoration in a production implementation.

The important point is that rollback should be tested and observable. It should not be a manual command someone invents during an incident.

## 10. Generative AI For SRE

I would use Generative AI to reduce operational toil and cognitive load:

- summarize incidents from alerts, logs, deploy history, and chat timelines
- retrieve relevant runbook sections
- draft postmortems from verified facts
- generate test cases for Python automation
- explain Terraform plans during review
- identify noisy alerts and suggest tuning
- provide a read-only ChatOps assistant for service state

The guardrails matter:

- read-only by default
- no secrets in prompts
- RBAC and audit logging
- human approval for destructive actions
- generated code still goes through tests, scanning, and review

AI should speed up investigation and routine work. It should not bypass operational controls.

## 11. Insider Risk Evaluation

I define insider risk as the potential for harm caused by trusted users or compromised trusted identities misusing or mishandling authorized access.

That includes:

- malicious insiders
- negligent users
- compromised accounts
- privilege misuse
- data exfiltration
- policy bypass
- risky behavior around sensitive systems or data

When evaluating an insider-risk platform, I look for:

- detection quality across malicious, negligent, and compromised-user scenarios
- peer-group baselining and behavioral analytics
- explainable risk scoring
- low false-positive burden
- visibility across endpoint, cloud, SaaS, server, and privileged-account activity
- privacy controls such as role-based access, pseudonymization, minimization, and audit trails
- SIEM, SOAR, ticketing, and identity-provider integrations
- operational scalability and endpoint performance

The platform has to produce explainable, prioritized, privacy-aware signals. Detecting events is not enough if analysts cannot trust or act on the results.

## 12. Summary

The main design principle is using each tool at the right layer:

- Terraform manages desired infrastructure state.
- Python coordinates safe deployment workflows around that state.
- Ansible makes host configuration repeatable.
- Docker makes the application artifact portable.
- GitHub Actions provides the controlled path from commit to deployment.

This gives me a repeatable infrastructure and application deployment model with validation, observability, and room to mature into stricter production controls.
