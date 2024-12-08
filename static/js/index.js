
function fullScreenCanvas(canvas) {
	canvas.width = window.innerWidth / 2

	canvas.height = window.innerHeight / 2

}

function clear_canvas(canvas, ctx) {
	ctx.fillStyle = "rgb(255,255,255)"
	ctx.fillRect(0, 0, canvas.width, canvas.height)
}


var socket = io();
const canvas = document.getElementById("ips_canvas")
const manual_scan_btn = document.getElementById("make_manual_scan_btn")
const toggle_calibration_btn = document.getElementById("toggle_calibration_btn")

const reset_receivers_btn = document.getElementById("reset_receivers_btn")

const calibration_holder = document.getElementById("calibration_holder")

manual_scan_btn.addEventListener("click", () => {
	let test_x = document.getElementById("x_cordinate").value

	let test_y = document.getElementById("y_cordinate").value

	out_obj = {
		x: test_x,
		y: test_y
	}
	console.log(out_obj)

	out_str = JSON.stringify(out_obj)

	console.log(out_str)

	socket.emit("make manual scan", out_str)
})

const automatic_scan_btn = document.getElementById("make_automatic_scan_btn")
automatic_scan_btn.addEventListener("click", () => {
	socket.emit("make automatic scan", "")
})
reset_receivers_btn.addEventListener("click", async () => {

	relative_path = "/post/testing/reset_receivers"
	const resp = await fetch(relative_path)
})

toggle_calibration_btn.addEventListener("click", async () => {
	relative_path = "/post/testing/calibrate"

	const resp = await fetch(relative_path)

	let resp_msg = await resp.json()
	calibration_holder.innerHTML = `Calibration mode set to ${resp_msg.mode}`

})

const basis_width = 1707 / 2
const basis_height = 791 / 2

let px_x_diff = (window.innerWidth / 2) / basis_width
let px_y_diff = (window.innerHeight / 2) / basis_height

const ctx = canvas.getContext("2d")

fullScreenCanvas(canvas)

const REAL_ROOM_WIDTH = 556
const REAL_ROOM_HEIGHT = 375


let room_width = (REAL_ROOM_WIDTH * px_x_diff) / 2
let room_height = (REAL_ROOM_HEIGHT * px_y_diff) / 2

class Pie {
	constructor(name, x, y, rgb_color, distance) {
		this.name = name
		this.real_x = x

		this.real_y = y
		this.x = this.real_x * px_x_diff / 2
		this.y = this.real_y * px_y_diff / 2
		this.rgb_color = rgb_color
		this.distance = distance
	}
	update_x_y() {
		this.x = this.real_x * px_x_diff / 2
		this.y = this.real_y * px_y_diff / 2
	}

}

let PIES = [new Pie("pie4", 0, 0, [125, 125, 255], 20), new Pie("pie2", REAL_ROOM_WIDTH, 0, [255, 125, 125], 20), new Pie("pie3", 335, REAL_ROOM_HEIGHT, [125, 255, 125], 20)]


clear_canvas(canvas, ctx)

function draw_room_outline(canvas, ctx) {
	let x1 = canvas.width / 2 - room_width / 2

	let y1 = canvas.height / 2 - room_height / 2

	ctx.strokeRect(x1, y1, room_width, room_height)
}
function draw_cirlce(x, y, r, color, ctx) {
	ctx.beginPath();
	ctx.arc(x, y, r, 0, 2 * Math.PI);
	ctx.fillStyle = `rgb(${color[0]},${color[1]},${color[2]})`;

	ctx.lineWidth = 1
	ctx.strokeStyle = `rgb(0,0,0)`;
	ctx.fill();
	ctx.stroke();
}

function draw_circle_outline(x, y, r, color, ctx) {
	ctx.beginPath();
	ctx.arc(x, y, r, 0, 2 * Math.PI);
	ctx.lineWidth = 4
	ctx.strokeStyle = `rgb(${color[0]},${color[1]},${color[2]})`;
	ctx.stroke();
}
function draw_all() {

	fullScreenCanvas(canvas)
	clear_canvas(canvas, ctx)



	px_x_diff = (window.innerWidth / 2) / basis_width
	px_y_diff = (window.innerHeight / 2) / basis_height

	room_width = (REAL_ROOM_WIDTH * px_x_diff) / 2
	room_height = (REAL_ROOM_HEIGHT * px_y_diff) / 2

	let x1 = canvas.width / 2 - room_width / 2

	let y1 = canvas.height / 2 - room_height / 2

	draw_room_outline(canvas, ctx)

	for (let i = 0; i < PIES.length; i++) {
		PIES[i].update_x_y()
		let pie = PIES[i]
		console.log(pie)

		draw_cirlce(pie.x + x1, pie.y + y1, 20, pie.rgb_color, ctx)

		draw_circle_outline(pie.x + x1, pie.y + y1, pie.distance / 2 + 20, pie.rgb_color, ctx)
	}
}

draw_room_outline(canvas, ctx)

draw_all()
window.addEventListener("resize", () => {
	draw_all()

})
socket.on("reception", (value) => {
	let real_val = JSON.parse(value)
	for (let i = 0; i < PIES.length; i++) {
		let pie = PIES[i]
		if (pie.name == real_val.host_name) {
			PIES[i].distance = real_val.distance * -1
		}

	}
	draw_all()

})
