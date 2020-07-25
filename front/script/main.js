const SEA_COLOR = "#256692";
const AREA_WIDTH = 3000;
const AREA_HEIGHT = 3000;
let DRAW_BORDERS = false;
const HOST = 'localhost:8000'
const TEXTURE_URL = `http://${HOST}/load_data`;
const WS_URL = `ws://${HOST}/ws`;

let action = {up: false, down: false, left: false, right: false, shot: false};
let last_action = {};
let send_movement = false;
let player_id = '';

let camera_offset_x = 0;
let camera_offset_y = 0;

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

    render_screen(player_data, all_data, effects) {


        if (player_data) {
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
            this.clean_field();
            all_data.forEach((elem) => {
                this.render_entity(elem)
            });

            effects.forEach((elem) => this.animation(elem))
            this.context.translate(-camera_offset_x, -camera_offset_y);
        } else {
            this.game_over('Game over')
        }
    }

    clean_field() {
        let img = new Image();
        img.src = `static/img/space_contrust.png`;
        this.context.drawImage(img, 0, 0, AREA_WIDTH, AREA_HEIGHT);
    }

    point(x, y, canvas) {
        canvas.beginPath();
        this.context.fillStyle = "rgb(52,251,6)";
        canvas.arc(x, y, 1, 0, 2 * Math.PI, true);
        canvas.fill();
    }

    game_over(text) {
        this.clean_field()
        this.context.fillStyle = "white";
        this.context.font = 'bold 33px Arial';
        this.context.fillText(text, this.screen_width / 2, this.screen_height / 2)
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
            this.context.fillStyle = "rgba(23,236,112,0.58)";
            this.context.strokeStyle = "rgb(23,236,112)";
            this.context.beginPath();
            this.context.moveTo(elem.bounds[elem.bounds.length - 1][0], elem.bounds[elem.bounds.length - 1][1]);
            this.context.outlineColor = "rgba(1,173,72,0.89)";
            elem.bounds.forEach((e) => {
                this.context.lineTo(e[0], e[1]);
            });
            this.context.fill();
        }
    }

    life_count(elem) {
        this.context.fillStyle = "black";
        this.context.fillRect(elem.x - elem.hp_max / 2 - 1, elem.aabb[1] - 20, elem.hp_max + 2, 10);
        this.context.fillStyle = "green";
        this.context.fillRect(elem.x - elem.hp_max / 2, elem.aabb[1] - 19, elem.hp, 8);
    }

    nick_name(elem) {
        this.context.fillStyle = "black";
        let width = this.context.measureText(elem.name).width;
        this.context.fillRect(elem.x - elem.hp_max / 2 - 1, elem.aabb[1] - 36, width + 10, 17);

        this.context.fillStyle = "white";
        this.context.font = 'bold 13px Arial';
        this.context.fillText(elem.name, elem.x - elem.hp_max / 2 + 2, elem.aabb[1] - 24, elem.hp_max)
    }

    animation(elem) {
        let animation = this.resource_data[elem.id]
        let img = new Image();
        img.src = `static/img/${animation.texture}`;
        let frame = animation.frames[elem.step]
        if (frame) {
            this.context.drawImage(img,
                frame.sx, frame.sy, frame.width, frame.height,
                elem.x - (frame.width / 2), elem.y - (frame.height / 2), frame.width, frame.height);
        }
    }
}


class Animation {
    constructor() {
        this.animation_pool = []
        this.duration = 1000
        this.step_duration = 200
    }

    add_events(list_events) {
        let now = Date.now()
        let ap = this.animation_pool
        list_events.forEach((eff) =>
            this.animation_pool.push({
                'id': eff.id,
                'x': eff.x,
                'y': eff.y,
                'start': now,
                'finish': now + this.duration
            })
        )
    }

    get_current_frames() {
        let now = Date.now()
        let res_anim = [];
        [...this.animation_pool].forEach((elem) => {
            if (Date.now() > elem.finish) {
                let index = this.animation_pool.indexOf(elem)
                this.animation_pool.splice(index, 1);
            } else {
                let step_number = ((now - elem.start) / this.step_duration >> 0)
                res_anim.push({'id': elem.id, 'x': elem.x, 'y': elem.y, 'step': step_number})
            }
        })
        return res_anim
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

function handle_message(event, render, animation) {
    let data = JSON.parse(event.data);
    if (typeof data.player_id === "string") {
        player_id = data.player_id;
    } else {
        let self_object = data.entities.find(function (elem) {
            return elem.id === player_id
        })
        animation.add_events(data.effects)
        render.render_screen(self_object, data.entities, animation.get_current_frames());
    }
}

function handle_close(event, render) {
    render.game_over('Connection closed')
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

function render_point(event) {
    console.log(`{"x": ${Math.round(event.x - camera_offset_x)}, "y": ${Math.round(event.y - camera_offset_y)}},`)
}

window.onload = function () {
    async function start() {
        let render = new Render()
        await render.init()
        let animator = new Animation()
        socket = new WebSocket(WS_URL)
        socket.addEventListener('message', event => handle_message(event, render, animator));
        socket.addEventListener('open', event => handle_open_socket(event));
        socket.addEventListener('close', event => handle_close(event, render));
        document.addEventListener('click', event => render_point(event))
        document.addEventListener('keydown', event => evaluate_movement(event, true));
        document.addEventListener('keyup', event => evaluate_movement(event, false));
    }

    start().then(function () {
        console.log("Game started")
    });
}
