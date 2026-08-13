Upload index.html, manifest.json and sw.js to a new public GitHub repository. Enable GitHub Pages from main /(root). Open the live page in Safari and choose Share > Add to Home Screen. Use BACKUP JSON regularly because data is stored locally on the device.

Build v19.9.0 — AI Card Intake Review Gate
- AI recognition now stages a candidate before stock entry.
- Recognition fields can be reviewed/corrected before approval.
- Approval is required before an AI candidate can be saved to Stock.
- Extended card metadata: set code, rarity, illustrator, review state and approval timestamp.
- Service-worker cache bumped so installed PWAs receive the update.


Build v19.14.0 — Approved Match Pricing Flow + Pricing Validation v2
- Permanent SKU and Purchase-ID high-water ledger; sold/deleted historical IDs are never reused.
- Duplicate SKU/Purchase-ID guard before Stock save.
- Intake sequence preview.
- Verified market pricing display from the recognition backend when exact-card pricing is available.
- Suggested GBP list price can prefill Target/eBay list price; seller remains in control.
- Import/restore a real Gengrail JSON backup into a separate test origin to seed its historical sequence ledger.


UI v19.14.0: Market pricing now lives inside MATCH APPROVED. USE SUGGESTED PRICE is optional and populates the editable Target/eBay list price. CONTINUE INTAKE works with or without selecting a price.
