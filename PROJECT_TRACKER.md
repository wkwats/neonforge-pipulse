# NeonForge PiPulse — Project Tracker

Created: 2026-02-28 (Africa/Nairobi)

## Vision

A beautiful, real-time Raspberry Pi telemetry dashboard served over FastAPI and accessible on the local network.

Primary outcome:
- Open `http://<pi-ip>:8090` from any device on LAN and monitor the Pi live.

## Current Status

✅ MVP complete and running

- Project folder: `/home/wkwats/NeonForge-PiPulse`
- App entrypoint: `app.py`
- UI template: `templates/index.html`
- Runtime env: `.venv`
- Server bind: `0.0.0.0:8090`
- Verified endpoint: `/api/stats`

## Features Implemented

- FastAPI backend with HTML dashboard route (`/`)
- JSON metrics endpoint (`/api/stats`)
- Live CPU usage (total + per-core)
- CPU temperature monitoring
- Memory and disk usage
- Load averages
- Network RX/TX counters
- Host identity info (hostname, IP, platform, arch, boot time)
- Beautiful neon-styled dashboard + charts (Chart.js)

## How to Run

```bash
cd /home/wkwats/NeonForge-PiPulse
. .venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8090
```

## Quick Test

- Dashboard: `http://127.0.0.1:8090`
- API: `http://127.0.0.1:8090/api/stats`

From LAN device:
- `http://10.0.0.119:8090`

## Next Improvements (Backlog)

- [ ] Add websocket push (lower latency than polling)
- [ ] Add dark/light theme toggle
- [ ] Add process list (top CPU/memory consumers)
- [ ] Add temperature/history sparklines per metric
- [ ] Add auth (basic token or password gate)
- [ ] Add systemd service file for auto-start on boot
- [ ] Add export button (JSON snapshot)

## Notes

- Uses local virtual environment because global pip is externally managed (PEP 668).
- If the dashboard becomes unreachable, first check whether uvicorn process is still running.
