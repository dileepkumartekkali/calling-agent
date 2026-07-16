"""FastAPI entrypoint for Render. Exposes:
  - GET  /health  -> Render health check
  - WS   /ws      -> Exotel Voicebot Applet points here (wss://<your-render-host>/ws)
"""
import os

import uvicorn
from fastapi import FastAPI, WebSocket

from agent import bot
from pipecat.runner.types import WebSocketRunnerArguments

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await bot(WebSocketRunnerArguments(websocket=websocket))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
