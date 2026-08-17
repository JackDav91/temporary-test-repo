from pathlib import Path
import re

# Stock recognition follow-up: one active candidate at a time + simplified grader confirmation.
# Keeps raw recogniser handlers intact; graded bridge only listens/cleans its own UI.

p=Path('graded-integration.js')
s=p.read_text()
if 'STOCK RECOGNITION UI v1.9' not in s or 'function addGradedImport' not in s:
    raise SystemExit('Safety stop: expected Stock UI v1.9 baseline')

# Simplify user-facing provisional