import asyncio
import time

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from starlette.websockets import WebSocket

from warship.entities import Player
from warship.game_state import GameState

app = FastAPI()
gl = GameState()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pl = Player()
    pl.set_socket(websocket)
    gl.add_player(pl)
    last = time.time()
    while True:
        data = await websocket.receive_json()
        curr = time.time()
        delta = float(curr - last)
        last = curr
        pl.set_movement(data)
        for player in gl.players:
            if pl!=player and pl.collision(player):
                break
        else:
            pl.next(delta)
        pls = []
        for player in gl.players:
            pls.append(player.get_info())
        for player in gl.players:
            await player.socket.send_json({'players': pls})


@app.on_event("startup")
async def startup_event():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)