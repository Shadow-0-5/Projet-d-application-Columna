# Projet-d-application-ISO-

## Setup pour télécharger et coder avec VScode sur BGA Studio 

Télécharger l'extension SFTP de natizyskunk.sftp (Version 1.16.3) - SFTP/FTP sync

Ensuite dans votre dossier projet de travail : 
- faire un dossier .vscode
- dans ce dossier faire un sftp.json 
- y mettre et completer : 

```json 
{
  "name": "BGA Studio",
  "host": "1.studio.boardgamearena.com",
  "protocol": "sftp",
  "port": 2022,
  "username": "TON_LOGIN",
  "password": "TON_PASSWD",
  "remotePath": "/NOM_DU_PROJET/",
  "uploadOnSave": true,
  "ignore": [".vscode", "node_modules", ".git"]
}
```

- le fermer (important) puis lancer la commande Ctrl - Shfit - P + sftp et lancer le "Download Project"

# Architecture cible

Notre but : 
- Frontend (HTML/CSS/JS) : L'interface utilisateur. Le joueur clique sur une case. Le JS envoie l'action au serveur via WebSocket (ex: {"action": "move", "from": "A2", "to": "A4"}). Il reçoit l'état du plateau en JSON et met à jour l'affichage.
- Backend (Python + WebSockets) : Votre code Python actuel. Il reçoit le coup via WebSocket, vérifie s'il est légal, met à jour la matrice du jeu, fait jouer l'IA si c'est son tour, et renvoie le nouvel état du plateau au(x) joueur(s).

### 1. Le Backend (Python)
- Utilisez la bibliothèque FastAPI (qui intègre les WebSockets nativement et s'apprend en 30 minutes).
- Le serveur maintient en mémoire un dictionnaire des parties en cours : parties = { "room_id_123": { "player_1": ws1, "player_2": ws2, "board": instance_de_votre_jeu } }.
- Quand un utilisateur se connecte avec un identifiant de salon, le serveur l'ajoute à la partie.


### 2. Le Système de Lien Direct 
- Pas besoin de comptes utilisateurs ni de gestion de session complexe.
Joueur 1 arrive sur le site, clique sur "Créer une partie".
- Le frontend génère un ID unique (ex: un hash ou une chaîne aléatoire comme partie_aX8z9).
- Le site redirige Joueur 1 vers monjeu.com/game.html?room=partie_aX8z9.
- Le JS extrait cet ID de l'URL et ouvre une connexion WebSocket dédiée : ws://serveur:8000/game/partie_aX8z9.
- Joueur 2 reçoit le lien, s'y connecte, le JS ouvre le même canal WebSocket. Le serveur voit que la pièce est pleine, le jeu commence.

### 3. Le Frontend (JS)
pas besoin de réinventer la logique du jeu. Il faut:  
Créer le design du plateau.
Utiliser l'API native du navigateur : const socket = new WebSocket('ws://...');.  
Écouter les messages (socket.onmessage) pour redessiner le plateau à chaque coup reçu.

Pourquoi FastAPI ??   
FastAPI gère les WebSockets de base de manière très performante.  
Le gros avantage : Votre IA, votre logique de jeu et votre serveur WebSocket sont dans le même écosystème (Python). Pas de traduction, pas de communication entre deux technos différentes. Tu importes ta classe Jeu directement dans ton fichier serveur.  
Le Verdict : Laissez tomber Node.js pour ce projet. utilisez l'API WebSocket native du navigateur en JavaScript (qui s'interface parfaitement avec FastAPI).


### Hébergement Internet & Gratuité : C'est possible ?
Pour le Frontend (Le site web) : 100% Gratuit et Simple : comme le front n'est que du HTML/CSS/JS statique (sans PHP), hébergeable gratuitement sur : GitHub Pages ou Vercel ou Netlify. C'est gratuit à vie, extrêmement rapide, et ils vous fournissent un lien HTTPS sécurisé.

Pour le Backend (Le serveur Python + WebSockets) : Les options gratuites
C'est ici que ça se corse un peu, car faire tourner un serveur H24 qui maintient des connexions WebSockets consomme des ressources.
Render.com : Propose une offre gratuite (Free Web Services). Parfait pour les projets étudiants. Attention : le serveur s'endort après 15 minutes d'inactivité. La première connexion peut prendre 30 secondes à charger, mais une fois réveillé, ça fonctionne très bien.
Koyeb : Une excellente alternative moderne avec une offre gratuite qui prend en charge Python et les WebSockets sans coupure brutale.


```
[Joueur 1] --(Crée salon)--> [Site Web (JS)] --(Génère ID)--> ID: "room_A8F"
    |                                                               |
(Se connecte au WS)                                        (Partage le lien)
    |                                                               |
    v                                                               v
[FastAPI Server] <=== (Canal WS "room_A8F" établi) ===> [Joueur 2]
 (Stocke l'état du jeu en RAM)
```
1. Génération : Joueur 1 clique sur "Créer". Le JS fait un Math.random() customisé pour générer un ID (ex: A8F).
2. Redirection : L'URL devient monjeu.com/game.html?room=A8F.
3. Connexion : Le JS se connecte au WebSocket : ws://mon-backend.render.com/ws/A8F.
4. Attente : Le serveur FastAPI reçoit la connexion, crée une clé "A8F" dans son dictionnaire de parties en cours, et attend le deuxième joueur.
5. Rejoint : Joueur 2 ouvre le lien partagé, son JS extrait A8F et se connecte au même endpoint. Le serveur voit que la partie est pleine, et envoie le signal START aux deux joueurs.


### Phase 1 : Local & Standardisation
- (Back) :  Le jeu doit être une classe encapsulée, ex jeu.jouer_coup("E2", "E4") et jeu.obtenir_plateau_json(). L'IA doit être une fonction qui prend l'état actuel et renvoie le meilleur coup.
- (Front) : une page HTML simple avec un plateau statique (en CSS/Grid). Pas besoin de design final, juste des cases cliquables qui affichent leurs coordonnées dans la console JS (ex: cliqué sur "B3").

### Phase 2 : Le "Hello World" du WebSocket
Vous montez un serveur FastAPI local minimal. Tentez de vous connecter depuis leur code JS en local (new WebSocket("ws://localhost:8000/ws/test")).
Objectif de validation : Quand on clique sur une case du site web, le JS envoie "Clic" au serveur Python, et le serveur Python répond "Bien reçu". Rien de plus pour l'instant.

### Phase 3 : Le Contrat d'Échange
Écrivez sur un document partagé la structure exacte des messages JSON.
Exemple : Le Front envoie toujours {"action": "MOVE", "from": "A1", "to": "A2"}. Le Back répond toujours en renvoyant tout le plateau : {"board": [["R", "N", "B", ...], [...]], "turn": "white", "error": null}.

### Phase 4 : L'Intégration de la logique
- Back : Vous branchez votre classe de jeu sur le serveur FastAPI. Dès qu'un message de mouvement valide arrive, vous mettez à jour le jeu, et vous renvoyez le nouveau plateau. Si c'est au tour de l'IA, vous déclenchez votre fonction IA et vous renvoyez le coup de l'IA dans la foulée.
- Front : Vos potes codent la fonction JS qui efface le plateau et le redessine entièrement dès qu'un JSON de mise à jour est reçu du WebSocket.

### Notes De Claude 

Le **WebSocket** en ws:// (non chiffré) ne fonctionnera pas si votre frontend est hébergé sur GitHub Pages / Vercel en HTTPS — les navigateurs bloquent les connexions mixed content. Il faudra utiliser wss:// (WebSocket sécurisé). Render fournit HTTPS automatiquement donc wss:// sera disponible.


**Ce qui manque dans l'architecture**  
La gestion de la déconnexion. Que se passe-t-il si un joueur ferme son onglet ?  
FastAPI lèvera une WebSocketDisconnect exception. Il faut la gérer explicitement pour ne pas laisser l'autre joueur bloqué indéfiniment.  
**Le tour de l'IA.**  
 L'architecture dit "si c'est au tour de l'IA, on déclenche la fonction IA" — mais si le Minimax est profond, il peut prendre plusieurs secondes. Pendant ce temps le WebSocket est bloqué. Il faudra lancer l'IA dans un thread séparé avec asyncio pour ne pas bloquer le serveur.