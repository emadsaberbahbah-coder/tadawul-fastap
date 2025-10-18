# main.py
from fastapi import FastAPI, Header, HTTPException
from typing import Optional, Dict, Any, List
import os, time

APP_TOKEN = os.environ.get("APP_TOKEN", "")  # You'll set this at deploy time
app = FastAPI(title="Tadawul FastAPI Bridge", version="v0.1")

def require_auth(authorization: Optional[str]):
    # If no token set on server, allow all (dev mode). If set, enforce.
    if not APP_TOKEN:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    if token != APP_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/health")
def health():
    return {"ok": True, "ts": int(time.time())}

# -------- Quotes endpoint (shape your Apps Script understands) ----------
@app.post("/v41/quotes")
@app.get("/v41/quotes")
def quotes(
    symbols: Optional[str] = None,
    cache_ttl: int = 60,
    Authorization: Optional[str] = Header(None)
) -> Dict[str, Any]:
    require_auth(Authorization)

    # Accept JSON body too (POST). For simplicity, GET with ?symbols=AAPL,1120.SR is enough.
    # This is a minimal stub that returns an empty dict. We'll wire real fetching later.
    data: Dict[str, Any] = {}
    if symbols:
        for s in [x.strip() for x in symbols.split(",") if x.strip()]:
            data[s] = {"symbol": s}  # minimal placeholder

    return {"data": data}

# -------- Charts endpoint (shape your Apps Script understands) ----------
@app.post("/v41/charts")
@app.get("/v41/charts")
def charts(
    symbols: Optional[str] = None,
    period1: Optional[int] = None,
    period2: Optional[int] = None,
    cache_ttl: int = 900,
    Authorization: Optional[str] = Header(None)
) -> Dict[str, Any]:
    require_auth(Authorization)

    # Minimal stub: empty series. We'll add real data later.
    out: Dict[str, List[Dict[str, Any]]] = {}
    if symbols:
        for s in [x.strip() for x in symbols.split(",") if x.strip()]:
            out[s] = []  # no data yet

    return {"data": out}
