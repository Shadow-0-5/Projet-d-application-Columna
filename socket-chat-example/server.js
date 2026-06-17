import express from 'express';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { Server } from 'socket.io';

const app = express();
const server = createServer(app);
const io = new Server(server);

app.use(express.static('public'));


io.on('connection', (socket) => {
    console.log('Un joueur s\'est connecté');
    socket.pseudo = socket.id;

    // 1. Le joueur demande à rejoindre une room spécifique
    socket.on('join-room', (roomId) => {
        
        // Socket.io gère la création automatiquement. 
        // Si la room n'existe pas, elle est créée. Si elle existe, le joueur la rejoint.
        socket.join(roomId);
        socket.currentRoom = roomId; // On stocke la room dans l'objet socket pour s'en souvenir

        console.log(`Le joueur ${socket.id} a rejoint la room : ${roomId}`);

        // Optionnel : On prévient les AUTRES joueurs de la room qu'un adversaire est arrivé
        socket.to(roomId).emit('opponent-joined', `L'adversaire a rejoint la partie.`);
    });

    // 2. Quand un message est envoye
    socket.on('chat message', (msg) => {
        console.log('message:' + msg);
        socket.to(socket.currentRoom).emit('chat message', socket.pseudo, msg);
    });

    socket.on('set-pseudo', (name) => {
        console.log(`${socket.id} a change son pseudo pour : ${name}`);
        socket.pseudo = name;
    });

    socket.on('disconnect', () => {
        console.log('Un joueur a quitté.');
    });
});

server.listen(3000, () => {
    console.log('Serveur prêt sur le port 3000');
});