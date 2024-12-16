
var socket = io();
const canvas = document.getElementById("ips_canvas")
const manual_scan_btn = document.getElementById("make_manual_scan_btn")
const toggle_calibration_btn = document.getElementById("toggle_calibration_btn")
const people_counter = document.getElementById("people_counter")
const ride_dropdown= document.getElementById("ride_dropdown")
const ride_button = document.getElementById("ride_select")

ride_button.addEventListener("click",async () => {
	let value = ride_dropdown.value
	console.log(value)
	const resp = await fetch ("/post/testing/ride", {
		headers: {
			"Content-Type": "application/json",
		},
		method: "POST",
		body: JSON.stringify({ value: value  }),
	});

})

document.addEventListener("DOMContentLoaded",async () => {
	let rides_txt = await fetch("/get/testing/get_rides")
	let rides = await rides_txt.json()
	for (let i = 0; i < rides.rides.length;i++) {

	let elem= document.createElement("option")
		elem.innerHTML = rides.rides[i]
		if (rides.rides[i] == rides.chosen_ride) {
			elem.selected = true
		}
		ride_dropdown.append(elem)
	}



})
function fullScreenCanvas(canvas) {
	canvas.width = window.innerWidth / 1.5

	canvas.height = window.innerHeight / 1.5

}

function clear_canvas(canvas, ctx) {
	ctx.fillStyle = "rgb(255,255,255)"
	ctx.fillRect(0, 0, canvas.width, canvas.height)
}



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

	let test_x = document.getElementById("x_cordinate").value

	let test_y = document.getElementById("y_cordinate").value

	out_obj = {
		x: test_x,
		y: test_y
	}
	console.log(out_obj)

	out_str = JSON.stringify(out_obj)

	console.log(out_str)

	socket.emit("make automatic scan", out_str)
})
reset_receivers_btn.addEventListener("click", async () => {

	relative_path = "/get/testing/reset_receivers"
	const resp = await fetch(relative_path)
})

toggle_calibration_btn.addEventListener("click", async () => {
	relative_path = "/get/testing/calibrate"

	const resp = await fetch(relative_path)

	let resp_msg = await resp.json()
	calibration_holder.innerHTML = `Calibration mode set to ${resp_msg.mode}`

})
const ratio = 4

const basis_width = 1707 / 2 
const basis_height = 791 / 2 

let px_x_diff = (window.innerWidth / 2) / basis_width
let px_y_diff = (window.innerHeight / 2) / basis_height

const ctx = canvas.getContext("2d")

fullScreenCanvas(canvas)

const REAL_ROOM_WIDTH = 1200 
const REAL_ROOM_HEIGHT = 1200 


let room_width = (REAL_ROOM_WIDTH * px_x_diff) / ratio
let room_height = (REAL_ROOM_HEIGHT * px_y_diff) / ratio

class Pie {
	constructor(name, x, y, rgb_color, distance) {
		this.name = name
		this.real_x = x

		this.real_y = y
		this.x = this.real_x * px_x_diff / ratio
		this.y = this.real_y * px_y_diff / ratio 
		this.rgb_color = rgb_color
		this.distance = distance
	}
	update_x_y() {
		this.x = this.real_x * px_x_diff / ratio
		this.y = this.real_y * px_y_diff / ratio
	}

}

let PIES = [new Pie("pie4", REAL_ROOM_WIDTH, 0, [125, 125, 255], 20), new Pie("pie2", REAL_ROOM_WIDTH/2, REAL_ROOM_HEIGHT, [255, 125, 125], 20), new Pie("pie3", 0, 0, [125, 255, 125], 20)]


clear_canvas(canvas, ctx)

function draw_room_outline(canvas, ctx) {
	let x1 = canvas.width / 2 - room_width / ratio

	let y1 = canvas.height / 2- room_height / ratio

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

	room_width = (REAL_ROOM_WIDTH * px_x_diff) / ratio
	room_height = (REAL_ROOM_HEIGHT * px_y_diff) / ratio

	let x1 = canvas.width / 2 - room_width / ratio

	let y1 = canvas.height / 2 - room_height / ratio

	draw_room_outline(canvas, ctx)

	for (let i = 0; i < PIES.length; i++) {
		PIES[i].update_x_y()
		let pie = PIES[i]
		console.log(pie)

		draw_cirlce(pie.x + x1, pie.y + y1, 20, pie.rgb_color, ctx)

		draw_circle_outline(pie.x + x1, pie.y + y1, pie.distance / 2, pie.rgb_color, ctx)
	}
}

draw_room_outline(canvas, ctx)

draw_all()
window.addEventListener("resize", () => {
	draw_all()

})
socket.on("reception", async (value) => {
	let real_val = await JSON.parse(value)
	for (let i = 0; i < PIES.length; i++) {
		let pie = PIES[i]
		if (pie.name == real_val.host_name) {
			PIES[i].distance = real_val.distance 
		}

	}
	let people = real_val.people
	people_counter.innerHTML = `People: ${people}`
	draw_all()

	for (let i = 0; i< real_val.people_locations.length;i++) {
		draw_cirlce(real_val.people_locations[i][0]*px_x_diff/ratio, real_val.people_locations[i][1]*px_y_diff/ratio, 5, [0,0,255], ctx)
	}


})
