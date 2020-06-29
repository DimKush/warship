const SEA_COLOR = "#256692";
const AREA_WIDTH = 3000;
const AREA_HEIGHT = 2000;

window.onload = function () {
    let screen_width = window.innerWidth
    let screen_height = window.innerHeight;
    let socket = new WebSocket("ws://localhost:8000/ws");
    let context;
    let action = {up: false, down: false, left: false, right: false, shot: false};
    let last_action = {};
    let send_movement = false;
    let player_id = '';

    let drawingCanvas = document.getElementById('screen');

    if (drawingCanvas && drawingCanvas.getContext) {
        context = drawingCanvas.getContext('2d');
        context.canvas.width  = screen_width;
        context.canvas.height = screen_height;
        clean_field()
    }

    function render_screen(player_data, all_data) {
        clean_field();
        let camera_offset_x = 0;
        let camera_offset_y = 0;
        if (player_data.x > (screen_width / 2)) {
            camera_offset_x = screen_width / 2 - player_data.x
        }
        if (player_data.x > AREA_WIDTH - (screen_width / 2)) {
            camera_offset_x = screen_width - AREA_WIDTH
        }
        if (player_data.y > (screen_height / 2)) {
            camera_offset_y = screen_height / 2 - player_data.y
        }
        if (player_data.y > AREA_HEIGHT - (screen_height / 2)) {
            camera_offset_y = screen_height - AREA_HEIGHT
        }
        context.translate(camera_offset_x, camera_offset_y);
        all_data.forEach((elem) => {
            render_bound_ship(elem.x, elem.y, elem.r, elem.bounds, elem.aabb, elem.type, elem.hp || '')
        });
        context.translate(-camera_offset_x, -camera_offset_y);
    }

    function clean_field() {
        context.fillStyle = SEA_COLOR;
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

    function point(x, y, canvas) {
        context.save();
        canvas.beginPath();
        context.fillStyle = "rgb(52,251,6)";
        canvas.arc(x, y, 1, 0, 2 * Math.PI, true);
        canvas.fill();
        canvas.restore();
    }

    function render_bound_ship(x, y, r, bounds, aabb, type, hp) {
        context.save();
        context.translate(x, y);
        context.rotate(r);
        let img = new Image();
        switch (type) {
            case 'Main ship':
                img.src = "static/img/tuna_main.png";
                context.drawImage(img, -25, -60, 49, 124);
                break;
            case 'Bullet':
                img.src = "static/img/bullet.png";
                context.drawImage(img, -6, -12, 12, 15);
                break;
        }
        context.restore();

        context.rect(aabb[0], aabb[1], aabb[2] - aabb[0], aabb[3] - aabb[1]);
        context.stroke();
        point(x, y, context)
    }

    function evaluate_movement(event, action_flag) {
        switch (event.keyCode) {
            case 65: // A
                action.left = action_flag; break;
            case 87: // W
                action.up = action_flag; break;
            case 68: // D
                action.right = action_flag; break;
            case 83: // S
                action.down = action_flag; break;
            case 32: // space
                action.shot = action_flag; break;
        }
        for (let key in action) {
            if (last_action[key] !== action[key]) {
                last_action[key] = action[key];
                send_movement = true;
            }
        }
    }
    document.addEventListener('keydown', event => evaluate_movement(event, true));
    document.addEventListener('keyup', event => evaluate_movement(event, false));

    socket.onopen = function () {
        setInterval(function () {
            if (send_movement) {
                socket.send(JSON.stringify(action));
                send_movement = false;
            }
        }, 100);
    }

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data);
        if (typeof data.player_id === "string") {
            player_id = data.player_id;
        } else {
            let self_object = data.entities.find(function (elem) {
                return elem.id === player_id
            })
            render_screen(self_object, data.entities);
        }
    };
}
