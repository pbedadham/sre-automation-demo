# Insider Risk Evaluation

## Definition

Insider risk is the potential for harm caused by trusted users, contractors, administrators, service accounts, or compromised trusted identities misusing or mishandling authorized access.

This includes:

- malicious data theft or sabotage
- negligent data exposure
- compromised account activity
- privilege misuse
- policy bypass attempts
- risky behavior that increases organizational exposure

## Evaluation Criteria

Detection quality:

- Detects malicious, negligent, and compromised-user patterns.
- Identifies unusual file access, data movement, cloud uploads, USB usage, and privilege misuse.
- Uses peer-group baselining and behavioral context.

Signal quality:

- Low false positive rate.
- Explainable risk scores.
- Clear evidence trail for investigations.
- Tunable policies without hiding real risk.

Coverage:

- Endpoints.
- Cloud and SaaS.
- Servers.
- Privileged sessions.
- Admin and service accounts.
- Remote and hybrid users.

Privacy and governance:

- Role-based investigator access.
- Audit logs for investigations.
- Data minimization.
- Policy controls for jurisdiction and labor requirements.
- Clear retention settings.

Operational integration:

- SIEM integration.
- SOAR integration.
- Ticketing integration.
- Alert routing.
- APIs for automation.
- Case management.

Enterprise readiness:

- Scale.
- Endpoint performance.
- High availability.
- Deployment flexibility.
- Compliance posture for government or regulated environments.

## Test Scenarios

- Employee downloads unusual volume of sensitive files before departure.
- Developer uploads source code to personal storage.
- Admin accesses critical systems outside peer-group norms.
- User attempts to bypass security controls.
- Compromised account logs in from unusual location and enumerates shares.
- Privileged user accesses data unrelated to role.

## Strong Evaluation Position

An effective insider-risk platform must balance detection, explainability, privacy, and operational usability. A tool that overwhelms analysts will fail operationally. A tool that produces opaque risk scores will not earn trust.
