import asyncio
import json
import os
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse, RedirectResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets import ConnectionClosedOK

from back.config import ENTITY_PATH, RPS
from back.game import Game

app = FastAPI()

origins = [
    "http://localhost", "http://127.0.0.1",
    "http://localhost:80",
    "http://localhost:8080",
    "https://localhost",
    "https://localhost:80",
    "https://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.gl = Game()
app.state.sockets = []

app.mount("/static", StaticFiles(directory="front"), name="static")
templates = Jinja2Templates(directory="front")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    app.state.sockets.append(websocket)

    player = app.state.gl.add_player()
    await websocket.send_json({'player_id': player.id})
    while True:
        try:
            data = await websocket.receive_json()
            if data.get('name'):
                player.name = data.get('name')
            else:
                ahead = angle = shot = 0
                if data['up']:
                    ahead = 1
                if data['down']:
                    ahead = -1
                if data['right']:
                    angle = - 1 if data['down'] else 1
                if data['left']:
                    angle = + 1 if data['down'] else -1
                if data['shot']:
                    shot = 1
                player.set_action(shot)
                player.set_moving(angle, ahead)
        except WebSocketDisconnect as e:
            print(f'WebSocketDisconnect: {e}')
            break
        except Exception as e:
            print(f'Error: {e}')
            break

    app.state.gl.del_player(player)
    if websocket in app.state.sockets:
        app.state.sockets.remove(websocket)
    await websocket.close()


@app.get("/")
async def main_menu(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/game")
async def main_menu(request: Request, user_name: str = ''):
    return templates.TemplateResponse("client.html", {"request": request, "name": user_name})


@app.get("/load_data")
async def load_data(request: Request):
    data = {}
    for root, dirs, files in os.walk(ENTITY_PATH):
        for name in files:
            f = open(os.path.join(root, name), 'r')
            obj = json.loads(f.read())
            context_id = obj.pop('context_id')
            data[context_id] = obj
    return JSONResponse(content=data)


@app.get("/favicon.ico")
async def favicon(request: Request):
    return RedirectResponse("/static/img/favicon.ico")


@app.on_event("startup")
async def startup_event():
    app.state.gl.init_scene()
    await start_background_tasks()


async def start_background_tasks():
    loop = asyncio.get_event_loop()
    loop.create_task(tick())
    loop.create_task(response_for_all())


async def tick():
    last = time.time()
    while True:
        curr = time.time()
        delta = float((curr - last))
        last = curr
        app.state.gl.exec_step(delta)

        pending = RPS - (time.time() - curr)
        await asyncio.sleep(RPS if pending < 0 else pending)


async def response_for_all():
    last = time.time()
    while True:
        curr = time.time()
        delta = float((curr - last))
        last = curr

        curr_state = app.state.gl.get_state()
        if curr_state:
            curr_state['frame_time'] = delta
            for socket in app.state.sockets:
                try:
                    await socket.send_json(curr_state)
                except ConnectionClosedOK as e:
                    print(f'Sending error (ConnectionClosedOK): {e}')
                except Exception as e:
                    print(f'Sending error: {e}')

        await asyncio.sleep(RPS)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, debug=True)
