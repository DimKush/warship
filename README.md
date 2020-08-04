# Steel rebbot
![Python Version](https://img.shields.io/badge/Python-3.8.2-green.svg)
### description
2d browser multiplayer game for PC about Space and Spaceships 

![Image of Space](front/img/demo.png)


### where to play
https://steel-rebbot.herokuapp.com/

### for developers

**run(prod):** `gunicorn -w 1 -k uvicorn.workers.UvicornWorker back.main:app `

**run(dev):** `python ./back/main.py` 