# Working on this distribution

Before installing, removing, troubleshooting, or changing this mod, read
[docs/AGENT_HANDOFF.md](docs/AGENT_HANDOFF.md), then README.md and manifest.json.
The handoff defines the supported packages, conflict handling, backup procedure,
runtime checks, and the cancelled shop/hero-grid scope.

Do not commit `.local/`, game configuration, user backups, or installation receipts.
Run `python -m unittest discover -s tests -v` before changing the management script.
