# Projet d'Application Columna 

Repository du projet d'Application 3A INSA 

## Architecture du projet

```text
.
├── jeuPython/
│   ├── img/
│   │   ├── board.jpg
│   │   ├── dalle1.jpg
│   │   ├── dalle2.jpg
│   │   ├── dalle3.jpg
│   │   ├── dalle4.jpg
│   │   ├── dalle5.jpg
│   │   ├── pion_blanc.png
│   │   └── pion_noir.png
│   ├── board.py
│   ├── main.py
│   └── player.py
│
└── siteColumna/
    ├── backend/
    │   ├── img/ (pyton + :)
    │   │   ├── bamboo.png
    │   │   ├── columna.svg
    │   │   ├── door.png
    │   │   ├── panda.png
    │   │   ├── robot.png
    │   │   └── wand.png
    │   ├── board.py
    │   ├── player.py
    │   ├── requirements.txt
    │   └── server.py
    └── frontend/
```

## Membres du Projet

| Username          | Name                              |
| ----------------- | --------------------------------- |
| slt0C0moi         | RAPINEL   Florian                 |
| Mat-La            | LAURENT   Mathis                  |
| Simon             | CREPIN    Simon                   |
| Shadow-0-5        | SCHREYECK Romain                  |

## Remarques

**IMPORTANT :** Dans le fichier **app.js** il faut modifier la **ligne 20** en insérant l'adresse web du serveur python. 


## Comment lancer l'IA Python localement ? 

Il suffit d'executer le **main.py** à la racine du projet.   
**NB** : Pour modifier la **profondeur de l'IA** _(nombre de coup calculé à l'avance)_ :  
La classe Player possède un attribut self.profondeur, à modifier lors de la création de l'objet Player _(avec le paramètre profondeur = X)_ dans le fichier **main.py** aux **lignes 24 & 25**.  
Il est également possible de changer les valeurs des points accordés lors de l'évaluation d'une position dans **Player.py**

## Commande de lancement du serveur python en local (Uvicorn) - Backend puis Front End

Dépendances à installer (Dans un environnement virtuel python de préférence) : 

```bash
# Suivre les étapes si dessous pour faire l'installation dans un environnement virtuel.
pip install fastapi uvicorn websockets
```

Création d'un environnement virtuel :   

```bash
# Créer l'environnement virtuel
python -m venv venv

# L'activer sous Windows (PowerShell)
.\venv\Scripts\Activate.ps1 

# Installation des dépendances
pip install fastapi uvicorn websockets
```


Commande à lancer depuis de le dossier **game_python** :  
```bash
 uvicorn server:app --host 0.0.0.0 --port 8000
 ```

 Enfin nous utilisons l'extension **Go live** de VSCode pour lancer le Front end : La page **index.html**.