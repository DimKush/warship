import asyncio
import time

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

from back.game import Game

app = FastAPI()
app.state.gl = Game()
app.state.sockets = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    app.state.sockets.append(websocket)

    player = app.state.gl.add_player()
    while True:
        data = await websocket.receive_json()
        ahead = angle = 0
        if data['up']:
            ahead = 1
        if data['down']:
            ahead = -1
        if data['right']:
            angle = 1
        if data['left']:
            angle = -1
        player.set_moving(angle, ahead)


@app.on_event("startup")
async def startup_event():
    await start_background_tasks()


async def start_background_tasks():
    asyncio.create_task(response_for_all())


async def response_for_all():
    last = time.time()
    while True:
        curr = time.time()
        delta = float((curr - last))
        last = curr
        app.state.gl.exec_step(delta)
        for socket in app.state.sockets:
            await socket.send_json(app.state.gl.get_state())
        await asyncio.sleep(0.016)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
