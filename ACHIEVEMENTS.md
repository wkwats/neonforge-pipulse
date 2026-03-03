# NeonForge PiPulse — Achievements Log

## 2026-03-03

### ✅ Major Refactor: Pi Stats → Home Sensor Hub
- Re-architected the app from Raspberry Pi host telemetry to a **sensor-first dashboard**.
- Introduced secure sensor ingestion endpoint: `POST /api/ingest` (API key protected).
- Added sensor data APIs:
  - `GET /api/sensors/latest`
  - `GET /api/sensors/history`
- Added SQLite persistence (`pipulse.db`) with index optimization.

### ✅ Dashboard UX Upgrade
- Rebuilt UI to focus on home sensors:
  - latest readings cards
  - sensor list panel
  - selectable history trend chart
- Improved header/badge alignment and right-side pill placement.
- Added human-friendly date formatting (with seconds), e.g. `Mar 3rd 2026 4:09:14am`.

### ✅ Reliability / Runtime
- Performed local smoke tests for ingest + read APIs.
- Restarted Uvicorn and validated live responses.
- Added no-store cache behavior on `/` to reduce stale frontend issues during iteration.

### ✅ Documentation
- Updated `README.md` to reflect new architecture, API usage, and startup flow.
- Added security notes for API key handling and deployment hardening.
