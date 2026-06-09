from pathlib import Path

from sre_automation.config import load_config


def test_load_config_resolves_relative_terraform_dir() -> None:
    config = load_config(Path("examples/config/dev.yaml"))

    assert config.name == "dev"
    assert config.service.name == "orders-api"
    assert config.service.port == 8080
    assert config.terraform_dir.name == "dev"
