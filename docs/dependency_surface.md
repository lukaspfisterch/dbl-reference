# Dependency surface

## dbl-ingress

Import roots:
- `dbl_ingress`
- `dbl_ingress.admission`
- `dbl_ingress.shaping`

Public entry points:
- `AdmissionRecord`
- `AdmissionError`
- `InvalidInputError`
- `shape_input`

Layer:
- Imported by gateway authority only.

Expectations:
- Admission validation is deterministic.
- Admission failures surface a stable reason code derived from the error taxonomy.
