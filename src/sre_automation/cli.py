from __future__ import annotations

import argparse

from sre_automation.config import load_config
from sre_automation.deploy import DeploymentOrchestrator, DeploymentRequest
from sre_automation.observability import configure_logging
from sre_automation.terraform import TerraformRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SRE automation deployment demo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("plan", "deploy"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--config", required=True, help="Path to environment YAML config")
        subparser.add_argument(
            "--image-tag",
            required=True,
            help="Immutable artifact tag to promote",
        )
        subparser.add_argument(
            "--previous-image-tag",
            help="Artifact tag to restore during rollback",
        )
        subparser.add_argument(
            "--dry-run",
            action="store_true",
            help="Log commands without executing them",
        )

    return parser


def main() -> None:
    configure_logging()
    args = build_parser().parse_args()
    config = load_config(args.config)
    request = DeploymentRequest(
        config=config,
        image_tag=args.image_tag,
        dry_run=args.dry_run,
        previous_image_tag=args.previous_image_tag,
    )
    orchestrator = DeploymentOrchestrator(terraform=TerraformRunner(dry_run=args.dry_run))

    if args.command == "plan":
        orchestrator.plan(request)
    elif args.command == "deploy":
        orchestrator.deploy(request)


if __name__ == "__main__":
    main()
