import pytest

from sre_automation.secrets import SecretResolver


def test_secret_resolver_accepts_secret_manager_refs() -> None:
    resolved = SecretResolver().resolve({"token": "vault://prod/orders-api/token"})

    assert resolved == {"token": "<resolved-at-runtime>"}


def test_secret_resolver_rejects_plaintext_refs() -> None:
    with pytest.raises(ValueError):
        SecretResolver().resolve({"token": "super-secret-value"})
