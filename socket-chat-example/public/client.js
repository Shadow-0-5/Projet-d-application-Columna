const form = document.getElementById('form');
const input = document.getElementById('input');
const messages = document.getElementById('messages');

const socket = io();

const urlParams = new URLSearchParams(window.location.search);
let roomId = urlParams.get('room');
let pseudo = "";

if (!roomId) {
    roomId = 'room-' + Math.random().toString(36).substr(2, 9);
    window.history.pushState({}, '', `?room=${roomId}`);
}

socket.emit('join-room', roomId);

form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (input.value) {
        if (input.value.startsWith("setPseudo:")) {
            pseudo = input.value.substring(10);
            socket.emit("set-pseudo", pseudo);
            input.value = '';
        }
        else {
            const item = document.createElement('li');
            item.textContent = pseudo + " : " + input.value;
            messages.appendChild(item);
            window.scrollTo(0, document.body.scrollHeight);
            socket.emit('chat message', input.value);
            input.value = '';
        }
    }
});

socket.on('chat message', (name, msg) => {
    const item = document.createElement('li');
    item.textContent = name + ' : ' + msg;
    messages.appendChild(item);
    window.scrollTo(0, document.body.scrollHeight);
});

socket.on('opponent-joined', (msg) => {
    alert("Quelqu'un s'est connecte!");
});