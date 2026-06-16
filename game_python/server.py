from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from board import Board
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

parties = {}

# Petite fonction maison pour extraire l'état du jeu en JSON
def get_board_state(board_instance):
    return {
        "dalles": board_instance.dalles,
        "white_pawns": board_instance.white_pawns,
        "black_pawns": board_instance.black_pawns
    }

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    if room_id not in parties:
        print(f"Création de la partie {room_id}")
        parties[room_id] = {
            "board": Board(screen=None),
            "clients": []
        }
    
    parties[room_id]["clients"].append(websocket)
    print(f"Un joueur a rejoint {room_id}. Total: {len(parties[room_id]['clients'])}")

    try:
        # Dès la connexion, on envoie le plateau initial pour synchroniser le joueur
        await websocket.send_json({
            "status": "sync",
            "state": get_board_state(parties[room_id]["board"])
        })

        while True:
            # On reçoit l'action du JS
            data = await websocket.receive_json()
            print(f"[{room_id}] Action reçue : {data}")
            
            # Si c'est un mouvement de pion ou d'empilement
            if data["action"] in ["move", "stack"]:
                # Le JS envoie des listes [y, x], Python veut des tuples (y, x)
                begin_pos = tuple(data["from"])
                end_pos = tuple(data["to"])
                
                # 💥 LA MAGIE EST ICI : On applique le coup dans ta logique Python
                parties[room_id]["board"].move(begin_pos, end_pos)
                
                # On prépare le nouveau plateau mis à jour
                new_state = {
                    "status": "update",
                    "state": get_board_state(parties[room_id]["board"])
                }
                
                # On broadcast (diffuse) le nouveau plateau à tous les joueurs du salon
                for client in parties[room_id]["clients"]:
                    await client.send_json(new_state)

    except Exception as e:
        print(f"Un joueur a quitté {room_id}.")
        parties[room_id]["clients"].remove(websocket)