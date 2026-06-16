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