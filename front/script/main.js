var socket = new WebSocket("ws://0.0.0.0:8000/ws");
var context;
var movement = {
    up: false,
    down: false,
    left: false,
    right: false
};
var last_movement = {};
var send_movement = false;
var player_id = '';
window.onload = function () {
    var drawingCanvas = document.getElementById('screen');
    if (drawingCanvas && drawingCanvas.getContext) {
        context = drawingCanvas.getContext('2d');
        clean_field()
    }

    function clean_field() {
        context.fillStyle = "#2a5d64";
        context.fillRect(0, 0, drawingCanvas.width, drawingCanvas.height)
    }

    function render_main_ship(x, y, r) {
        context.fillStyle = "#b41909";
        context.save();
        context.translate(x + 3, y + 8);
        context.rotate(r * Math.PI / 180);
        context.fillRect(0, 0, 12, 32);
        context.restore();
    }

    function render_ship(x, y, r) {
        context.fillStyle = "#2c383c";
        context.save();
        context.translate(x - 3, y + 16);
        context.rotate(r * Math.PI / 180);
        context.fillRect(+ 3, 0, 12, 32);
        context.restore();
    }

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data);
        if (typeof data.player_id === "string") {
            player_id = data.player_id;
        } else {
            clean_field();
            data.forEach((elem) => {
                if (elem.id == player_id) {
                    render_main_ship(elem.x, elem.y, elem.r);
                } else {
                    render_ship(elem.x, elem.y, elem.r);
                }
            });

        }
    };

    document.addEventListener('keydown', function (event) {
        evaluateMovement(event, true);
    });
    document.addEventListener('keyup', function (event) {
        evaluateMovement(event, false);
    });

    function evaluateMovement(event, direction_flag) {
        switch (event.keyCode) {
            case 65: // A
                movement.left = direction_flag;
                break;
            case 87: // W
                movement.up = direction_flag;
                break;
            case 68: // D
                movement.right = direction_flag;
                break;
            case 83: // S
                movement.down = direction_flag;
                break;
        }
        if (!(last_movement.up === movement.up &&
            last_movement.down === movement.down &&
            last_movement.right === movement.right &&
            last_movement.left === movement.left)) {
            for (var key in movement) {
                last_movement[key] = movement[key];
            }
            send_movement = true;
        }
    }

    socket.onopen = function () {
        setInterval(function () {
            if (send_movement) {
                socket.send(JSON.stringify(movement));
                send_movement = false;
            }
        }, 100);
    };

};
class Game {
    constructor() {
        this.socket = new WebSocket("ws://0.0.0.0:8000/ws_red");
        this.context = null;
        this.movement = {
            up: false,
            down: false,
            left: false,
            right: false
        };
        this.last_movement = {};
    }
}

