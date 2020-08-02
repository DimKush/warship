# Steel rebbot
### descripltion
2d browser multiplayer game for PC about Space and Spaceships 

![Image of Space](https://github.com/dIgor93/warship/blob/master/front/img/demo.PNG)


### where to play
https://steel-rebbot.herokuapp.com/

### for developers
**language:** python 3.8

**run(prod):** `gunicorn -w 1 -k uvicorn.workers.UvicornWorker back.main:app `

**run(dev):** `python ./back/main.py` 