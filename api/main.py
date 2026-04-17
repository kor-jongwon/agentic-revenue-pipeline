from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys

# Add parent directory to sys.path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.vector_store import ARPVectorStore

app = FastAPI(title="ARP Dashboard API")
templates = Jinja2Templates(directory="templates")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_PATH = "transaction_logs.json"
SNAPSHOT_DIR = "data_snapshots"
vector_store = ARPVectorStore()

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/stats")
def get_stats():
    """Returns overall pipeline statistics."""
    # We simulate reading from monitor data or shared memory
    # For now, reading transaction logs
    if not os.path.exists(LOG_PATH):
        return {"total_cycles": 0, "success_rate": "0%", "total_value": 0}
    
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        logs = json.load(f)
        
    total = len(logs)
    successes = sum(1 for log in logs if log.get("success"))
    total_value = sum(float(log.get("value", 0)) for log in logs)
    
    return {
        "total_cycles": total,
        "success_rate": f"{(successes/total*100):.1f}%" if total > 0 else "0%",
        "total_value": round(total_value, 2),
        "last_updated": logs[-1].get("timestamp") if total > 0 else None
    }

@app.get("/logs")
def get_logs(limit: int = 20):
    """Returns recent logs."""
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        logs = json.load(f)
    return logs[::-1][:limit]

@app.get("/search")
def search_insights(q: str):
    """Search the vector database."""
    results = vector_store.query(q)
    return results

@app.get("/snapshot/{filename}")
def get_snapshot(filename: str):
    """Read a specific data snapshot."""
    file_path = os.path.join(SNAPSHOT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Snapshot not found")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
