from __future__ import annotations

from sre_automation.config import EnvironmentConfig
from sre_automation.observability import event


def rollback(config: EnvironmentConfig, previous_image_tag: str | None, dry_run: bool) -> None:
    event(
        "rollback_started",
        environment=config.name,
        service=config.service.name,
        previous_image_tag=previous_image_tag,
        dry_run=dry_run,
    )
    if previous_image_tag is None:
        event("rollback_skipped", reason="no previous artifact recorded", environment=config.name)
        return

    event(
        "rollback_completed",
        environment=config.name,
        service=config.service.name,
        restored_image_tag=previous_image_tag,
    )
