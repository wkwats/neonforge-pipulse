# ⚡ NeonForge PiPulse

Sensor-first home telemetry dashboard built with **FastAPI**.

---

## What it is now

PiPulse is now focused on **house sensors** (temperature, humidity, motion, etc.) instead of Pi host stats.

- Ingest sensor readings via API
- Store data in local SQLite (`pipulse.db`)
- View latest values + 6h trend chart in neon dashboard UI

---

## Tech Stack

- FastAPI
- Uvicorn
- Jinja2 templates
- SQLite (stdlib)
- Chart.js

---

## Quick Start

```bash
cd /home/wkwats/NeonForge-PiPulse
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn jinja2
export PIPULSE_INGEST_API_KEY="replace-with-strong-key"
uvicorn app:app --host 0.0.0.0 --port 8090
```

Open dashboard:
- `http://127.0.0.1:8090`

---

## API

### `POST /api/ingest`
Add one sensor reading.

Header:
- `x-api-key: <PIPULSE_INGEST_API_KEY>`

Body example:

```json
{
  "sensor_id": "living-room-esp32",
  "metric": "temperature",
  "value": 27.4,
  "unit": "°C",
  "location": "living room"
}
```

### `GET /api/sensors/latest`
Returns latest reading per `sensor_id + metric`.

### `GET /api/sensors/history?sensor_id=...&metric=...&minutes=360`
Returns historical points for charting.

---

## Notes

- Default API key fallback is `change-me` — **always set your own key** before deployment.
- For internet exposure, place behind HTTPS reverse proxy and add stronger auth.
