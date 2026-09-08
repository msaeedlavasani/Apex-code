# AC-DEV-021 — Evidence Receipt Validator v1

Status: `VERIFIED` / `PROVEN`

Task: `AC-DEV-021`

## Result

The repository now provides a pure `validate_receipt()` contract, a file-based
`validate_receipt_file()` helper, and the bounded CLI
`scripts/validate_receipts.py`. Validation is read-only and fail-closed; it
never edits a receipt, registry, mapping, or claim state.

The durable validation-run receipt is
[`AC-DEV-021-VALIDATION-RECEIPT-0026.json`](AC-DEV-021-VALIDATION-RECEIPT-0026.json).

## Checks

- secret-shaped keys and obvious private-key/token patterns are rejected;
- schema version, receipt type, required identity, and closed claim vocabulary
  are checked;
- operational observations and reconciliation mapping changes are compared to
  the current Agent/Skill Registry;
- repository-contained evidence references are checked when a repository root
  is supplied;
- `ADMITTED`, blocked, Human Gate, dispatch, side-effect, permanent-selection,
  and explicit `SOURCE_ID_ASC` policy fields are checked;
- promotion from `NOT_PROVEN` or `UNKNOWN` requires explicit demonstrated
  runtime evidence and is never performed by the validator.

The two AC-DEV-019 receipts validate successfully at registry revision 2.
Negative fixtures for secret fields, invalid claims, registry mismatch,
unauthorized tie-breaking, and unsupported promotion are rejected.

No ECC installation, executor selection, dispatch, or authority transfer was
introduced.
