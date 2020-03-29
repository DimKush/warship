var socket = new WebSocket("ws://0.0.0.0:8000/ws");
var context;

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
    function unrender_ship(x, y) {
        context.fillStyle = "#2a5d64";
        context.fillRect(x-1, y-1, 12, 32)

    }
    function render_ship(x, y) {
        context.fillStyle = "#2c383c";
        context.fillRect(x, y, 10, 30)

    }

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data);
        data = data['players'];
        for (var i=0; i<old_players.length; i++) {
            unrender_ship(old_players[i]['x'], old_players[i]['y'])
        }
        for (var i=0; i<data.length; i++) {
            render_ship(data[i]['x'], data[i]['y'])
        }
        old_players = data;

    };

    socket.onopen = function () {
        setInterval(function () {
            socket.send(JSON.stringify(movement))
        }, 100);
    };
    var old_players = [];
    var movement = {
        up: false,
        down: false,
        left: false,
        right: false
    };
    document.addEventListener('keydown', function (event) {
        switch (event.keyCode) {
            case 65: // A
                movement.left = true;
                break;
            case 87: // W
                movement.up = true;
                break;
            case 68: // D
                movement.right = true;
                break;
            case 83: // S
                movement.down = true;
                break;
        }
    });
    document.addEventListener('keyup', function (event) {
        switch (event.keyCode) {
            case 65: // A
                movement.left = false;
                break;
            case 87: // W
                movement.up = false;
                break;
            case 68: // D
                movement.right = false;
                break;
            case 83: // S
                movement.down = false;
                break;
        }
    });


};