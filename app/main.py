import time

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    x = y = 0
    last = 0
    while True:
        _curr = time.time()

        data = await websocket.receive_json()

        curr = time.time()
        delta = float((curr - last)) * 80
        last = curr
        if data['up']:
            y -= delta
        if data['down']:
            y += delta
        if data['left']:
            x -= delta
        if data['right']:
            x += delta

        await websocket.send_json({"x": x, "y": y})
        _last = time.time()
        print(_last - _curr)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)