"""Authentication towards Kraftringen."""

__package__ = "auth"

# Explicitly export classes, disable linting rule not in favor
# Flake 8 (F401), however, needs to be per-line
# pylint: disable=useless-import-alias

from auth.auth import Authorizer as Authorizer  # noqa: F401
