# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-02-26
### Added
- Initial public release of `TROEL OPS Kit` CLI workflow.
- End-to-end pipeline: ingest, validate, KPI, alerts, report.
- Synthetic demo data generator.
- Recruiter-focused documentation and repository hygiene files.

### Changed
- Technical rebrand from legacy `supplykit` naming to:
  - package: `troel_ops_kit`
  - distribution: `troel-ops-kit`
  - CLI command: `troel-ops`
- Added structured-ish logging and mypy configuration.

### Fixed
- Markdown report template loader/package path.
- Robust handling for empty validation issues.
