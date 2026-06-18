import random
import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from board import Board
from player import Player # Import de ton IA

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

parties = {}

def get_board_state(partie):
    return {
        "dalles": partie["board"].dalles,
        "white_pawns": partie["board"].white_pawns,
        "black_pawns": partie["board"].black_pawns,
        "turn": partie["turn"],
        "phase": partie["phase"]
    }

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, mode: str = "multi"):
    await websocket.accept()
    
    if room_id not in parties:
        print(f"Création de la partie {room_id} (Mode: {mode})")
        parties[room_id] = {
            "board": Board(screen=None),
            "clients": [],         # Liste de WebSockets purs
            "roles": {},           # Dictionnaire {websocket: role}
            "turn": "white" if mode == "ia" else "waiting",
            "phase": "move",
            "mode": mode,
            "ia": Player(color="black", IA=True) if mode == "ia" else None
        }
    
    # 1. Attribuer les couleurs
    nb_joueurs = len(parties[room_id]["clients"])
    
    if parties[room_id]["mode"] == "ia":
        role = "white" if nb_joueurs == 0 else "spectator"
    else:
        if nb_joueurs == 0:
            role = "white"
        elif nb_joueurs == 1:
            role = "black"
            # Lancement du tirage au sort à l'arrivée du deuxième joueur
            parties[room_id]["turn"] = random.choice(["white", "black"])
        else:
            role = "spectator"
            
    # Stockage propre des structures séparées
    parties[room_id]["clients"].append(websocket)
    parties[room_id]["roles"][websocket] = role

    try:
        # Synchro de début de partie
        if parties[room_id]["turn"] != "waiting":
            print(f"La partie {room_id} commence ! Premier joueur : {parties[room_id]['turn']}")
            for client in parties[room_id]["clients"]:
                client_role = parties[room_id]["roles"].get(client, "spectator")
                await client.send_json({
                    "status": "sync",
                    "role": client_role,
                    "state": get_board_state(parties[room_id])
                })
        else:
            await websocket.send_json({
                "status": "sync",
                "role": role,
                "state": get_board_state(parties[room_id])
            })

        while True:
            data = await websocket.receive_json()
            
            if data["action"] in ["move", "stack"]:
                parties[room_id]["board"].move(tuple(data["from"]), tuple(data["to"]))
                
                if data["action"] == "move":
                    parties[room_id]["phase"] = "stack"
                elif data["action"] == "stack":
                    parties[room_id]["phase"] = "move"
                    parties[room_id]["turn"] = "black" if parties[room_id]["turn"] == "white" else "white"
                
                # Diffusion aux clients connectés
                new_state = {
                    "status": "update",
                    "state": get_board_state(parties[room_id])
                }
                for client in parties[room_id]["clients"]:
                    await client.send_json(new_state)

                # ==========================================
                # 🤖 DECLENCHEMENT DE L'IA
                # ==========================================
                if parties[room_id]["mode"] == "ia" and parties[room_id]["turn"] == "black":
                    print("L'IA réfléchit...")
                    
                    ia_player = parties[room_id]["ia"]
                    le_board = parties[room_id]["board"]
                    
                    action = await asyncio.to_thread(ia_player.take_action, le_board)
                    
                    if action:
                        move_action, stack_action = action
                        parties[room_id]["board"].move(move_action[0], move_action[1])
                        parties[room_id]["board"].move(stack_action[0], stack_action[1])
                        
                        parties[room_id]["turn"] = "white"
                        parties[room_id]["phase"] = "move"
                        
                        print("L'IA a joué :", action)
                        
                        new_state_ia = {
                            "status": "update",
                            "state": get_board_state(parties[room_id])
                        }
                        for client in parties[room_id]["clients"]:
                            await client.send_json(new_state_ia)
                    else:
                        print("L'IA n'a plus de coups possibles !")

    except Exception as e:
        print(f"Déconnexion ou canal fermé : {e}")
    finally:
        # Nettoyage sécurisé à l'aide de blocs d'appartenance conditionnels
        if room_id in parties:
            if websocket in parties[room_id]["clients"]:
                parties[room_id]["clients"].remove(websocket)
            if websocket in parties[room_id]["roles"]:
                del parties[room_id]["roles"][websocket]