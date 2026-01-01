# Admission and rejection

## Admission ownership

Admission lives in the gateway authority layer.
The canonical admission library is `dbl-ingress`.
Boundary and UI components never perform admission.

## Reason codes

Reason codes are defined by `dbl-ingress` and form the unified catalog.
The gateway maps admission failures to a stable reason code string.

Rejection shape:
- HTTP 4xx
- body includes `reason_code` as a stable string

## Reason-code stability

Reason codes are part of the public contract.
Changes require explicit compatibility notes in this repo.
