from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
            data = await websocket.receive_json()
            print(f"[Salon {room_id}] Action reçue : {data}")
            
            reponse = {
                "status": "success",
                "message": "Le serveur a bien reçu ton action",
                "action_recue": data
            }
            await websocket.send_json(reponse)
    except Exception as e:
        print(f"Le joueur s'est déconnecté. {e}")