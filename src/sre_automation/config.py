from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ServiceConfig:
    name: str
    port: int
    health_url: str


@dataclass(frozen=True)
class EnvironmentConfig:
    name: str
    region: str
    terraform_dir: Path
    service: ServiceConfig
    secret_refs: dict[str, str]
    approval_required: bool
    min_healthy_instances: int


def load_config(path: str | Path) -> EnvironmentConfig:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        raw: dict[str, Any] = yaml.safe_load(handle)

    repo_root = (
        config_path.parents[2]
        if config_path.parts[-3:-1] == ("examples", "config")
        else Path.cwd()
    )
    terraform_dir = Path(raw["terraform_dir"])
    if not terraform_dir.is_absolute():
        terraform_dir = repo_root / terraform_dir

    service = raw["service"]
    return EnvironmentConfig(
        name=raw["environment"],
        region=raw["region"],
        terraform_dir=terraform_dir,
        service=ServiceConfig(
            name=service["name"],
            port=int(service["port"]),
            health_url=service["health_url"],
        ),
        secret_refs=dict(raw.get("secret_refs", {})),
        approval_required=bool(raw.get("approval_required", False)),
        min_healthy_instances=int(raw.get("min_healthy_instances", 1)),
    )
