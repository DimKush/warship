const SEA_COLOR = "#256692";
const AREA_WIDTH = 3000;
const AREA_HEIGHT = 2000;
let DRAW_BORDERS = true;
const TEXTURE_URL = 'http://localhost:8000/load_data';

let action = {up: false, down: false, left: false, right: false, shot: false};
let last_action = {};
let send_movement = false;
let player_id = '';

class Render {
    constructor() {
        this.drawingCanvas = document.getElementById('screen');
        this.screen_width = window.innerWidth;
        this.screen_height = window.innerHeight;
        if (this.drawingCanvas && this.drawingCanvas.getContext) {
            this.context = this.drawingCanvas.getContext('2d');
            this.context.canvas.width = this.screen_width;
            this.context.canvas.height = this.screen_height;
        }
        this.resource_data = null
    }

    async init() {
        this.resource_data = await fetch(TEXTURE_URL)
            .then((res) => res.json())
            .catch(err => {
                throw err
            });
    }

    render_screen(player_data, all_data) {
        this.clean_field();
        let camera_offset_x = 0;
        let camera_offset_y = 0;
        if (player_data.x > (this.screen_width / 2)) {
            camera_offset_x = this.screen_width / 2 - player_data.x
        }
        if (player_data.x > AREA_WIDTH - (this.screen_width / 2)) {
            camera_offset_x = this.screen_width - AREA_WIDTH
        }
        if (player_data.y > (this.screen_height / 2)) {
            camera_offset_y = this.screen_height / 2 - player_data.y
        }
        if (player_data.y > AREA_HEIGHT - (this.screen_height / 2)) {
            camera_offset_y = this.screen_height - AREA_HEIGHT
        }
        this.context.translate(camera_offset_x, camera_offset_y);
        all_data.forEach((elem) => {
            this.render_entity(elem)
        });
        this.context.translate(-camera_offset_x, -camera_offset_y);
    }

    clean_field() {
        this.context.fillStyle = SEA_COLOR;
        this.context.fillRect(0, 0, this.screen_width, this.screen_height)
    }

    point(x, y, canvas) {
        canvas.beginPath();
        this.context.fillStyle = "rgb(52,251,6)";
        canvas.arc(x, y, 1, 0, 2 * Math.PI, true);
        canvas.fill();
    }

    render_entity(elem) {
        this.context.save();
        this.context.translate(elem.x, elem.y);
        this.context.rotate(elem.r);

        let obj = this.resource_data[elem.context_id]
        let img = new Image();
        img.src = `static/img/${obj.texture}`;
        this.context.drawImage(img, obj.offset_x, obj.offset_y, obj.width, obj.height);
        this.context.restore();

        switch (elem.type) {
            case 'Player':
                this.life_count(elem)
                this.nick_name(elem)
                break
        }

        if (DRAW_BORDERS) {
            this.context.rect(elem.aabb[0], elem.aabb[1], elem.aabb[2] - elem.aabb[0], elem.aabb[3] - elem.aabb[1]);
            this.context.stroke();
            this.point(elem.x, elem.y, this.context)
            this.context.fillStyle = "rgba(85,97,90,0.58)";
            this.context.beginPath();
            this.context.moveTo(elem.bounds[elem.bounds.length - 1][0], elem.bounds[elem.bounds.length - 1][1]);
            elem.bounds.forEach((e) => {
                this.context.lineTo(e[0], e[1]);
            });
            this.context.fill();
        }
    }

    life_count(elem) {
        this.context.fillStyle = "green";
        this.context.fillRect(elem.x - elem.hp / 2, elem.aabb[1] - 20, elem.hp, 10);
    }

    nick_name(elem) {
        this.context.fillStyle = "white";
        this.context.font = 'bold 20px Arial';
        this.context.fillText(elem.name, elem.x - elem.hp_max / 2, elem.aabb[1] - 30, elem.hp_max)
    }
}


function evaluate_movement(event, action_flag) {
    switch (event.keyCode) {
        case 65: // A
            action.left = action_flag;
            break;
        case 87: // W
            action.up = action_flag;
            break;
        case 68: // D
            action.right = action_flag;
            break;
        case 83: // S
            action.down = action_flag;
            break;
        case 32: // space
            action.shot = action_flag;
            break;
    }
    for (let key in action) {
        if (last_action[key] !== action[key]) {
            last_action[key] = action[key];
            send_movement = true;
        }
    }
}

function handle_message(event, render) {
    let data = JSON.parse(event.data);
    if (typeof data.player_id === "string") {
        player_id = data.player_id;
    } else {
        let self_object = data.entities.find(function (elem) {
            return elem.id === player_id
        })
        render.render_screen(self_object, data.entities);
    }
}

function handle_open_socket(event) {

    socket.send(JSON.stringify({'name': player_name}));
    setInterval(function () {
        if (send_movement) {
            socket.send(JSON.stringify(action));
            send_movement = false;
        }
    }, 100);
}

window.onload = function () {
    async function start() {
        let render = new Render()
        await render.init()
        socket = new WebSocket("ws://localhost:8000/ws")
        socket.addEventListener('message', event => handle_message(event, render));
        socket.addEventListener('open', event => handle_open_socket(event));
        document.addEventListener('keydown', event => evaluate_movement(event, true));
        document.addEventListener('keyup', event => evaluate_movement(event, false));
    }

    start().then(function () {
        console.log("Game started")
    });
}
