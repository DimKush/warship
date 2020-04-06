import asyncio
import time

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

from back.game_state import GameState

app = FastAPI()
gl = GameState()
app.state.sockets = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    app.state.sockets.append(websocket)

    player_id = gl.add_player()
    await websocket.send_json({'player_id': player_id})
    while True:
        data = await websocket.receive_json()
        ahead = delta_angle = 0
        if data['up']: ahead = 1
        if data['down']: ahead = -1
        if data['right']: delta_angle = 1
        if data['left']: delta_angle = -1
        gl.set_player_direction(player_id, ahead, delta_angle)


@app.on_event("startup")
async def startup_event():
    await start_background_tasks()


async def start_background_tasks():
    asyncio.create_task(send_status())


async def send_status():
    last = time.time()
    g = 0
    while True:
        curr = time.time()
        delta = float((curr - last))
        last = curr
        gl.exec_step(delta)
        for socket in app.state.sockets:
            await socket.send_json(gl.get_state())
        await asyncio.sleep(0.016)
        # if (g % 100 == 0):
        #     print(gl.get_state())
        # g += 1


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)