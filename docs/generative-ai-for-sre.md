# Generative AI For SRE

## Recommended Uses

- Summarize incidents from alerts, logs, deploy history, and chat timelines.
- Retrieve runbook sections relevant to a current alert.
- Draft postmortems from verified incident facts.
- Generate unit tests for Python automation.
- Explain unfamiliar Terraform plans during review.
- Recommend alert tuning based on historical noise.
- Provide a read-only ChatOps assistant for service state.

## Agentic Workflow Example

```text
Alert fires
  |
  v
AI assistant gathers context:
  - alert payload
  - service owner
  - recent deploys
  - top log errors
  - dashboard links
  - runbook entries
  |
  v
Incident brief for human responder
  |
  v
Human approves any remediation
  |
  v
Bounded automation executes action and records audit trail
```

## Guardrails

- Default to read-only access.
- Require human approval for destructive or production-mutating actions.
- Enforce RBAC and environment boundaries.
- Keep audit logs for prompts, retrieved context, recommendations, and actions.
- Never send secrets to the model.
- Use retrieval from trusted internal docs and source repositories.
- Require tests, policy checks, and code review for generated code.

## Positioning

AI should reduce cognitive load and operational toil. It should not bypass change management, access control, or review.
