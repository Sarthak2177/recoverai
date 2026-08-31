"""
RecoverAI — FastAPI Server
"""
import json
import asyncio
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from agent.graph import recovery_agent

app = FastAPI(title="RecoverAI Agent Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

queue = asyncio.Queue()
_is_processing = False

def load_transactions():
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "transactions.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

async def process_batch():
    global _is_processing
    if _is_processing:
        return
    _is_processing = True
    
    txns = load_transactions()
    if not txns:
        await queue.put({"type": "error", "message": "No transactions found. Run synthetic data generator."})
        _is_processing = False
        return

    batch_id = "batch_" + os.urandom(4).hex()
    await queue.put({"type": "batch_start", "total": len(txns)})
    
    for i, txn in enumerate(txns):
        config = {"configurable": {"thread_id": f"{batch_id}_{txn['id']}"}}
        initial_state = {"transaction": txn, "transaction_id": txn["id"], "batch_id": batch_id}
        
        try:
            async for event in recovery_agent.astream(initial_state, config=config, stream_mode="values"):
                if "audit_log" in event and event["audit_log"]:
                    latest_log = event["audit_log"][-1]
                    await queue.put({
                        "type": "audit_event",
                        "txn_id": event["transaction_id"],
                        "status": event.get("recovery_status", "pending"),
                        "log": latest_log,
                        "progress": int(((i + 1) / len(txns)) * 100)
                    })
        except Exception as e:
            await queue.put({"type": "error", "message": f"Error processing {txn['id']}: {str(e)}"})
            
        await asyncio.sleep(0.5)

    await queue.put({"type": "batch_complete"})
    _is_processing = False

@app.get("/")
async def root():
    index_path = os.path.join(frontend_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/start")
async def start_processing():
    global _is_processing
    if not _is_processing:
        asyncio.create_task(process_batch())
        return {"status": "started"}
    return {"status": "already_running"}

@app.get("/api/stream")
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            try:
                message = await asyncio.wait_for(queue.get(), timeout=1.0)
                yield {"data": json.dumps(message)}
            except asyncio.TimeoutError:
                yield {"data": json.dumps({"type": "ping"})}
    return EventSourceResponse(event_generator())
