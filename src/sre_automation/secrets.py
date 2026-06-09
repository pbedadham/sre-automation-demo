from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class SecretResolver:
    """Demo resolver that validates secret references without reading secret values."""

    def resolve(self, refs: dict[str, str]) -> dict[str, str]:
        resolved = {}
        for name, ref in refs.items():
            if not ref.startswith(("aws-secretsmanager://", "gcp-secretmanager://", "vault://")):
                raise ValueError(f"unsupported secret reference for {name}: {ref}")
            log.info("validated secret reference", extra={"secret_name": name, "secret_ref": ref})
            resolved[name] = "<resolved-at-runtime>"
        return resolved
