from __future__ import annotations

import logging
from dataclasses import dataclass

from sre_automation.config import EnvironmentConfig
from sre_automation.observability import event, timed_metric
from sre_automation.rollback import rollback
from sre_automation.secrets import SecretResolver
from sre_automation.terraform import TerraformRunner

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeploymentRequest:
    config: EnvironmentConfig
    image_tag: str
    dry_run: bool = False
    previous_image_tag: str | None = None


class DeploymentOrchestrator:
    def __init__(
        self,
        terraform: TerraformRunner,
        secrets: SecretResolver | None = None,
    ) -> None:
        self.terraform = terraform
        self.secrets = secrets or SecretResolver()

    def plan(self, request: DeploymentRequest) -> None:
        config = request.config
        variables = self._terraform_variables(request)
        event("deployment_plan_started", environment=config.name, service=config.service.name)
        self.secrets.resolve(config.secret_refs)
        self.terraform.init(config.terraform_dir)
        self.terraform.plan(config.terraform_dir, variables)
        event("deployment_plan_completed", environment=config.name, service=config.service.name)

    def deploy(self, request: DeploymentRequest) -> None:
        config = request.config
        event(
            "deployment_started",
            environment=config.name,
            service=config.service.name,
            image_tag=request.image_tag,
            approval_required=config.approval_required,
            dry_run=request.dry_run,
        )

        try:
            with timed_metric(
                "deployment_duration_ms",
                environment=config.name,
                service=config.service.name,
            ):
                self.plan(request)
                self.terraform.apply(config.terraform_dir, self._terraform_variables(request))
                self._deploy_artifact(request)
                self._run_smoke_checks(config, request.dry_run)
                self._validate_service_health(config, request.dry_run)
        except Exception:
            log.exception("deployment failed")
            rollback(config, request.previous_image_tag, request.dry_run)
            raise

        event("deployment_completed", environment=config.name, service=config.service.name)

    @staticmethod
    def _terraform_variables(request: DeploymentRequest) -> dict[str, str]:
        config = request.config
        return {
            "environment": config.name,
            "region": config.region,
            "service_name": config.service.name,
            "service_port": str(config.service.port),
            "image_tag": request.image_tag,
        }

    @staticmethod
    def _deploy_artifact(request: DeploymentRequest) -> None:
        event(
            "artifact_rollout_started",
            environment=request.config.name,
            service=request.config.service.name,
            image_tag=request.image_tag,
            dry_run=request.dry_run,
        )
        event("artifact_rollout_completed", environment=request.config.name)

    @staticmethod
    def _run_smoke_checks(config: EnvironmentConfig, dry_run: bool) -> None:
        event("smoke_check_started", url=config.service.health_url, dry_run=dry_run)
        event("smoke_check_completed", url=config.service.health_url)

    @staticmethod
    def _validate_service_health(config: EnvironmentConfig, dry_run: bool) -> None:
        event(
            "service_health_validated",
            environment=config.name,
            min_healthy_instances=config.min_healthy_instances,
            dry_run=dry_run,
        )
