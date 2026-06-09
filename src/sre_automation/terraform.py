from __future__ import annotations

import logging
import subprocess
import time
from pathlib import Path

from sre_automation.observability import event, timed_metric

log = logging.getLogger(__name__)


class TerraformRunner:
    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run

    def init(self, directory: Path) -> None:
        self._run(["terraform", "init", "-input=false"], directory, retries=3)

    def plan(self, directory: Path, variables: dict[str, str]) -> None:
        cmd = ["terraform", "plan", "-input=false", *self._var_args(variables)]
        self._run(cmd, directory)

    def apply(self, directory: Path, variables: dict[str, str]) -> None:
        cmd = ["terraform", "apply", "-input=false", "-auto-approve", *self._var_args(variables)]
        self._run(cmd, directory)

    def _run(self, cmd: list[str], cwd: Path, retries: int = 1) -> None:
        with timed_metric("terraform_command_duration_ms", command=cmd[1], directory=str(cwd)):
            for attempt in range(1, retries + 1):
                event(
                    "command_started",
                    cmd=cmd,
                    cwd=str(cwd),
                    attempt=attempt,
                    dry_run=self.dry_run,
                )
                if self.dry_run:
                    return
                try:
                    subprocess.run(cmd, cwd=cwd, check=True)
                    event("command_completed", cmd=cmd, cwd=str(cwd), attempt=attempt)
                    return
                except subprocess.CalledProcessError:
                    if attempt == retries:
                        log.exception("command failed after retries")
                        raise
                    time.sleep(2**attempt)

    @staticmethod
    def _var_args(variables: dict[str, str]) -> list[str]:
        args: list[str] = []
        for key, value in variables.items():
            args.append(f"-var={key}={value}")
        return args
