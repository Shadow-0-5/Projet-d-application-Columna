from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from board import Board

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
        "turn": partie["turn"],   # Le serveur dicte à qui de jouer
        "phase": partie["phase"]  # Le serveur dicte la phase (move/stack)
    }

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    if room_id not in parties:
        parties[room_id] = {
            "board": Board(screen=None),
            "clients": [],
            "turn": "white",
            "phase": "move"
        }
    
    # 1. Attribuer les couleurs selon l'ordre d'arrivée
    nb_joueurs = len(parties[room_id]["clients"])
    if nb_joueurs == 0:
        role = "white"
    elif nb_joueurs == 1:
        role = "black"
    else:
        role = "spectator" # Le 3ème ne peut que regarder
        
    parties[room_id]["clients"].append(websocket)

    try:
        # 2. On envoie l'état ET le RÔLE au joueur
        await websocket.send_json({
            "status": "sync",
            "role": role,
            "state": get_board_state(parties[room_id])
        })

        while True:
            data = await websocket.receive_json()
            
            if data["action"] in ["move", "stack"]:
                parties[room_id]["board"].move(tuple(data["from"]), tuple(data["to"]))
                
                # 3. Le serveur change de phase et de tour
                if data["action"] == "move":
                    parties[room_id]["phase"] = "stack"
                elif data["action"] == "stack":
                    parties[room_id]["phase"] = "move"
                    # On inverse le tour
                    parties[room_id]["turn"] = "black" if parties[room_id]["turn"] == "white" else "white"
                
                new_state = {
                    "status": "update",
                    "state": get_board_state(parties[room_id])
                }
                
                # On broadcast (diffuse) le nouveau plateau
                for client in parties[room_id]["clients"]:
                    await client.send_json(new_state)

    except Exception as e:
        parties[room_id]["clients"].remove(websocket)