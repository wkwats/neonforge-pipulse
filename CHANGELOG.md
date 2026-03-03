# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Planned
- Sensor alert rules and Telegram notifications
- Device registration and metadata management
- Multi-metric overlays in trend charts

## [0.2.0] - 2026-03-03

### Added
- New `POST /api/ingest` endpoint for sensor data ingestion (API key protected)
- New `GET /api/sensors/latest` endpoint for latest sensor metrics
- New `GET /api/sensors/history` endpoint for metric history
- SQLite-backed storage (`pipulse.db`) with index for sensor/time queries
- `ACHIEVEMENTS.md` project progress log

### Changed
- Refactored app from Raspberry Pi host telemetry to sensor-first home dashboard
- Reworked frontend for sensor cards, sensor list, and selectable trend chart
- Improved header status pill alignment (right-aligned)
- Human-readable timestamps with seconds (e.g., `Mar 3rd 2026 4:09:14am`)
- Updated `README.md` for the new architecture and APIs

### Security
- Added API key enforcement for ingestion endpoint
- Added note to require strong `PIPULSE_INGEST_API_KEY` before deployment

### DevOps
- Added `pipulse.db` to `.gitignore`

## [0.1.0] - 2026-02-28

### Added
- Initial FastAPI dashboard for Raspberry Pi telemetry
- `/api/stats` endpoint with CPU, temp, memory, disk, network and host info
- Neon-themed UI with Chart.js visualizations
