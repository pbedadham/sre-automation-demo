# Observability Design

## Goals

The stack should answer three questions quickly:

- Is the service healthy for users?
- What changed recently?
- Where should the responder look next?

## Metrics

Use RED metrics for request-driven services:

- Rate: requests per second.
- Errors: 4xx/5xx and domain-specific failures.
- Duration: p50, p95, p99 latency.

Use USE metrics for infrastructure:

- Utilization: CPU, memory, disk, network.
- Saturation: queue depth, connection pool exhaustion, throttling.
- Errors: kernel errors, disk errors, network resets.

Use SLO signals:

- Availability.
- Latency objectives.
- Error-budget burn rate.
- Dependency health.

## Logs

Emit structured JSON logs with:

- service
- environment
- version
- request ID
- trace ID
- user-safe correlation ID
- event name
- outcome

Avoid sensitive values in logs. Prefer references, hashes, or redacted fields.

## Traces

Use OpenTelemetry for distributed tracing across:

- API gateway
- service handlers
- database calls
- queues
- external API calls

Sample normal traffic and retain higher detail for errors or slow requests.

## Reporting

Dashboards should be audience-specific:

- On-call: active incidents, alerts, recent deploys, dependency health.
- Engineering: latency, error rate, saturation, rollback rate.
- Leadership: SLO compliance, incident count, MTTR, error-budget burn.

## Alerting Principles

Prefer user-impacting alerts over noisy resource thresholds:

- High 5xx rate.
- Error-budget burn.
- Queue age exceeding user-facing objective.
- Deployment failed or rollback failed.
- Critical dependency unavailable.
