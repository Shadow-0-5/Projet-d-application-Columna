// Fonction pour générer un ID unique aléatoire (ex: 8x3f9a)
function generateRoomID() {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
}

let hideJoinInputTimeout = null;
const joinInput = document.getElementById("form-rejoindre");

function hideJoinInput() {
    if (!joinInput.value.trim()) {
        joinInput.type = 'hidden';
    }
}

function resetHideJoinInputTimer() {
    if (hideJoinInputTimeout) {
        clearTimeout(hideJoinInputTimeout);
    }
    hideJoinInputTimeout = setTimeout(hideJoinInput, 3000);
}

function joinRoom(event) {
    if (event) event.preventDefault();
    const roomID = joinInput.value;
    console.log(roomID);
    if (!roomID || !roomID.trim()) {
        return false;
    }
    window.location.href = `game.html?room=${roomID.trim()}`;
    return false;
}

// 1. Créer une partie
document.getElementById("btn-creer").addEventListener("click", function() {
    const roomID = generateRoomID();
    window.location.href = `game.html?room=${roomID}`;
});

// 2. Rejoindre une partie
document.getElementById("btn-rejoindre").addEventListener("click", function() {
    joinInput.type = 'text';
    joinInput.focus();
    resetHideJoinInputTimer();
});

joinInput.addEventListener('input', resetHideJoinInputTimer);
joinInput.addEventListener('focus', resetHideJoinInputTimer);

// 3. Jouer contre l'IA
document.getElementById("btn-ia").addEventListener("click", function() {
    const roomID = generateRoomID();
    window.location.href = `game.html?room=${roomID}&mode=ia`;
});

document.querySelectorAll(".btn").forEach((button) => {
  button.addEventListener("click", () => {
    button.animate(
      [
        { transform: "scale(1)" },
        { transform: "scale(.94)" },
        { transform: "scale(1)" }
      ],
      {
        duration: 180,
        easing: "ease-out"
      }
    );
  });
});
