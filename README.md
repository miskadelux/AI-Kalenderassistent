# AI-Kalenderassistent

Python-version: 3.13.5

## Databasinstallation

För att skapa tabeller och databasstruktur för händelser, kör schemat i MySQL:

```bash
# genom att köra
SOURCE #path_to_your_file
```

# Miljövariablar

skapa en .env fil med följande variabler

```
DB_HOST=localhost
DB_USER=din_användarmednamn
DB_PASSWORD=ditt_losenord
DB_NAME=ai_kalender


#OLLAMA inställningar
OLLAMA_HOST="web_path_to_localhost_with:port_number"
OLLAMA_MODEL="llama3:latest"
```
