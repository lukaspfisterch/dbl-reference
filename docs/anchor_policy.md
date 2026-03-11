# Anchor Policy

This repository is an anchor.

Allowed changes:
- Fixes to invariant enforcement when tests reveal a mismatch with the papers or dbl-core.
- Clarifications that reduce ambiguity without changing semantics.
- Updates strictly required by upstream contract changes (dbl-core, kernel-logic).

Forbidden changes:
- New features, integrations, storage backends, adapters, workflows.
- New event kinds, digest rules, canonicalization variants.
- Convenience APIs that expand the public surface.

Operational rule:
- Prefer keeping changes in dbl-main or domain runners.
- ensdg only moves when the authoritative sources moved.
