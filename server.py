"""FastAPI entrypoint for Render. Exposes:
  - GET  /health  -> Render health check
  - WS   /ws      -> Exotel Voicebot Applet points here (wss://<your-render-host>/ws)

UNVERIFIED: `WebsocketRunnerArguments` is my best recollection of Pipecat's raw-websocket
runner-args class, but I could not confirm the exact name against current docs (repeated
529s from the doc site while building this). Before deploying, run:
    python -c "from pipecat.runner.types import WebsocketRunnerArguments"
If that import fails, check `pipecat.runner.types` for the correct class name/kwarg
and fix the one line below in the websocket route.
"""
import os

import uvicorn
from fastapi import FastAPI, WebSocket

from agent import bot
from pipecat.runner.types import WebsocketRunnerArguments

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await bot(WebsocketRunnerArguments(websocket=websocket))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
