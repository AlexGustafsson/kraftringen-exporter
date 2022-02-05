"""Kraftringen API."""

__package__ = "kraftringen"

# Explicitly export classes, disable linting rule not in favor
# Flake 8 (F401), however, needs to be per-line
# pylint: disable=useless-import-alias

from kraftringen.bankid_auth import BankIDAuthorizer as BankIDAuthorizer  # noqa: F401
from kraftringen.api import API as API  # noqa: F401
