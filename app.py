from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="NeonForge PiPulse")

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "pipulse.db"
API_KEY = os.getenv("PIPULSE_INGEST_API_KEY", "change-me")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def _pretty_dt(value: str) -> str:
    try:
        d = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone()
    except Exception:
        return value

    day = d.day
    if 11 <= day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    return f"{d.strftime('%b')} {day}{suffix} {d.year} {d.strftime('%I:%M:%S%p').lstrip('0').lower()}"


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db() -> None:
    with _db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                metric TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                location TEXT,
                recorded_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_sensor_metric_time
            ON sensor_readings(sensor_id, metric, recorded_at)
            """
        )


@app.on_event("startup")
def startup() -> None:
    _init_db()


@app.get("/")
async def dashboard(request: Request):
    response = templates.TemplateResponse("index.html", {"request": request})
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response


@app.post("/api/ingest")
async def ingest_reading(
    payload: dict[str, Any], x_api_key: str | None = Header(default=None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    sensor_id = str(payload.get("sensor_id", "")).strip()
    metric = str(payload.get("metric", "")).strip()

    if not sensor_id or not metric:
        raise HTTPException(status_code=400, detail="sensor_id and metric are required")

    try:
        value = float(payload.get("value"))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="value must be numeric")

    unit = payload.get("unit")
    location = payload.get("location")
    recorded_at = payload.get("recorded_at") or datetime.now(timezone.utc).isoformat()

    with _db() as conn:
        conn.execute(
            """
            INSERT INTO sensor_readings(sensor_id, metric, value, unit, location, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (sensor_id, metric, value, unit, location, recorded_at),
        )

    return JSONResponse({"ok": True})


@app.get("/api/sensors/latest")
async def sensors_latest():
    with _db() as conn:
        rows = conn.execute(
            """
            SELECT sensor_id, metric, value, unit, location, recorded_at
            FROM sensor_readings r
            WHERE id = (
                SELECT id FROM sensor_readings
                WHERE sensor_id = r.sensor_id AND metric = r.metric
                ORDER BY recorded_at DESC, id DESC
                LIMIT 1
            )
            ORDER BY sensor_id, metric
            """
        ).fetchall()

    items = []
    for row in rows:
        item = dict(row)
        item["recorded_at_pretty"] = _pretty_dt(str(item.get("recorded_at", "")))
        items.append(item)

    now_iso = datetime.now(timezone.utc).isoformat()
    return JSONResponse(
        {
            "items": items,
            "count": len(items),
            "now": now_iso,
            "now_pretty": _pretty_dt(now_iso),
        }
    )


@app.get("/api/sensors/history")
async def sensor_history(
    sensor_id: str = Query(..., min_length=1),
    metric: str = Query(..., min_length=1),
    minutes: int = Query(360, ge=5, le=10080),
):
    since = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()

    with _db() as conn:
        rows = conn.execute(
            """
            SELECT recorded_at, value
            FROM sensor_readings
            WHERE sensor_id = ? AND metric = ? AND recorded_at >= ?
            ORDER BY recorded_at ASC
            """,
            (sensor_id, metric, since),
        ).fetchall()

    return JSONResponse(
        {
            "sensor_id": sensor_id,
            "metric": metric,
            "points": [dict(row) for row in rows],
        }
    )
