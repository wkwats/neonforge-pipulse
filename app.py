from datetime import datetime
import os
import platform
import socket

import psutil
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="NeonForge PiPulse")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


def _local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def _cpu_temp_c() -> float:
    temps = psutil.sensors_temperatures(fahrenheit=False)
    if not temps:
        return 0.0
    for entries in temps.values():
        if entries:
            return round(float(entries[0].current), 1)
    return 0.0


@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/stats")
async def stats_api():
    cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
    cpu_total = round(psutil.cpu_percent(interval=None), 1)

    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    net = psutil.net_io_counters()
    boot = datetime.fromtimestamp(psutil.boot_time())

    payload = {
        "hostname": socket.gethostname(),
        "ip": _local_ip(),
        "platform": platform.platform(),
        "arch": platform.machine(),
        "cpu_total": cpu_total,
        "cpu_per_core": [round(v, 1) for v in cpu_per_core],
        "cpu_temp_c": _cpu_temp_c(),
        "load_avg": [round(v, 2) for v in os.getloadavg()],
        "memory": {
            "used_gb": round(mem.used / (1024 ** 3), 2),
            "total_gb": round(mem.total / (1024 ** 3), 2),
            "percent": round(mem.percent, 1),
        },
        "disk": {
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "percent": round(disk.percent, 1),
        },
        "network": {
            "bytes_sent_mb": round(net.bytes_sent / (1024 ** 2), 2),
            "bytes_recv_mb": round(net.bytes_recv / (1024 ** 2), 2),
        },
        "boot_time": boot.strftime("%Y-%m-%d %H:%M:%S"),
        "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return JSONResponse(payload)
