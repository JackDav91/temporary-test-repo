Gengrail Business Log v19.15.0 — Inline Pricing Flow

Changes
- Market Pricing now renders inside the AI candidate review immediately after recognition.
- USE SUGGESTED PRICE is optional and can be selected before continuing intake.
- CONTINUE INTAKE approves the reviewed match, pre-fills the editable purchase form, and scrolls to it.
- Price remains blank when the user continues without choosing the suggestion.
- Permanent SKU/Purchase ledger remains active.
- Stale GEN000001 / PUR000001 generation placeholders have been removed from the intake form.
- Service worker cache bumped to v19.15.0.

Safety
Nothing is written to Stock until the existing final save/add-to-stock action is used.
