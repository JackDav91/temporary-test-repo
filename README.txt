Gengrail Business Log v19.16.0 — Pricing Calculator AI Refactor

Major changes
- Pricing Calculator is now the home for AI card recognition and market valuation.
- Scan/import a raw Pokémon single directly inside Pricing Calculator.
- Verified card identity and market evidence are shown compactly without the stock-intake form.
- Market value auto-populates when reliable pricing is available, but remains editable.
- Calculator now shows guided sell price, maximum target buy price, estimated profit, ROI and BUY / CONSIDER / PASS guidance.
- Removed stock write-back / listing-style actions from Pricing Calculator.
- Opportunity Finder remains a separate buying-opportunity module; live eBay feed is not part of this frontend release.
- Service worker cache bumped to v19.16.0.

Backend dependency
- For improved English exact-card pricing (including Evolving Skies-style cases), deploy Gengrail Card AI v1.7.0 before this frontend.
