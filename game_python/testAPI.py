from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser ton frontend local à parler à ton backend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    print("Un joueur s'est connecté !")
    try:
        while True:
            # On reçoit directement du JSON (FastAPI le transforme en dictionnaire Python)
            data = await websocket.receive_json()
            print(f"[Salon {room_id}] Action reçue : {data}")
            
            # On simule une réponse structurée en JSON pour l'instant
            reponse = {
                "status": "success",
                "message": "Le serveur a bien reçu ton action",
                "action_recue": data
            }
            await websocket.send_json(reponse)
    except Exception as e:
        print("Le joueur s'est déconnecté.")