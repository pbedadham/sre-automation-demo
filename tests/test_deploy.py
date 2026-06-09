from sre_automation.config import EnvironmentConfig, ServiceConfig
from sre_automation.deploy import DeploymentOrchestrator, DeploymentRequest


class FakeTerraform:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def init(self, _directory) -> None:
        self.calls.append("init")

    def plan(self, _directory, _variables) -> None:
        self.calls.append("plan")

    def apply(self, _directory, _variables) -> None:
        self.calls.append("apply")


def test_deploy_runs_plan_before_apply(tmp_path) -> None:
    terraform = FakeTerraform()
    config = EnvironmentConfig(
        name="dev",
        region="us-west-2",
        terraform_dir=tmp_path,
        service=ServiceConfig(name="orders-api", port=8080, health_url="https://example/health"),
        secret_refs={"db_password": "aws-secretsmanager://dev/orders-api/db_password"},
        approval_required=False,
        min_healthy_instances=1,
    )

    orchestrator = DeploymentOrchestrator(terraform=terraform)  # type: ignore[arg-type]
    orchestrator.deploy(DeploymentRequest(config=config, image_tag="sha-test", dry_run=True))

    assert terraform.calls == ["init", "plan", "apply"]
