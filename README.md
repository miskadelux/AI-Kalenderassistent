# AI-kalenderassistent

En Flask-baserad AI-kalenderassistent med MySQL som databas och Ollama för lokal AI-funktionalitet.

## Teknikstack

- Python 3.13.5
- Flask
- MySQL
- PyMySQL
- Ollama
- Requests
- python-dotenv
- Ruff

## Projektstruktur

```text
AI-kalenderassistent/
│
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── health.py
│   │
│   ├── __init__.py
│   ├── config.py
│   └── db.py
│
├── database/
├── python/
│   └── tests/
│       ├── test_connection.py
│       └── test_ollama.py
│
├── sprintar/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Installation

### 1. Klona projektet

```bash
git clone <repository-url>
cd AI-kalenderassistent
```

### 2. Skapa virtuell miljö

```bash
python -m venv venv
```

Aktivera miljön i PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Installera beroenden

```bash
python -m pip install -r requirements.txt
```

## Databasinstallation

Se till att MySQL är installerat och körs.

Skapa databasen `ai_kalender` och kör SQL-schemat som finns i projektets `database/`-katalog.

Exempel i MySQL-klienten:

```sql
SOURCE sökväg/till/schema.sql;
```

## Miljövariabler

Skapa en `.env`-fil i projektets rotkatalog.

Exempel:

```env
DB_HOST=localhost
DB_USER=din_användare
DB_PASSWORD="ditt_lösenord"
DB_NAME=ai_kalender

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3:latest
```

Samtliga variabler är obligatoriska.

Applikationen kontrollerar variablerna vid uppstart och avbryter starten om någon saknas.

**Viktigt:** `.env` innehåller känsliga uppgifter och ska inte publiceras i Git.

Om du ändrar miljövariabler medan Flask körs behöver applikationen startas om.

## Ollama – lokal AI-modell

1. Installera Ollama.
2. Starta Ollama.
3. Hämta önskad modell:

```bash
ollama pull llama3
```

Kontrollera installerade modeller:

```bash
ollama list
```

Kontrollera att Ollama fungerar med det manuella testskriptet:

```bash
python python/tests/test_ollama.py
```

## Starta applikationen

Aktivera den virtuella miljön och kör:

```bash
python run.py
```

Flask startar på:

```text
http://127.0.0.1:5000
```

## API – Health Check

Applikationen har en hälsokontroll på:

```http
GET /health
```

Kontrollen verifierar:

- MySQL: anslutning genom SQL-frågan `SELECT 1`.
- Ollama: tillgänglighet via `/api/tags`.
- Ollama-modell: kontrollerar att konfigurerad modell finns installerad.

Ingen AI-generering utförs under hälsokontrollen.

### Testa hälsokontrollen

```powershell
curl.exe -i http://127.0.0.1:5000/health
```

### Exempel på lyckat svar

```json
{
  "status": "healthy",
  "components": {
    "mysql": {
      "status": "connected",
      "response_time_ms": 25.0
    },
    "ollama": {
      "status": "reachable",
      "response_time_ms": 20.0
    }
  }
}
```

### Statusar

| Övergripande status | Betydelse                           |
| ------------------- | ----------------------------------- |
| `healthy`           | Alla komponenter fungerar           |
| `degraded`          | Minst en komponent har problem      |
| `unhealthy`         | Ingen komponent är fullt fungerande |

### MySQL-statusar

- `connected`
- `authentication_failed`
- `database_access_denied`
- `database_not_found`
- `server_unavailable`
- `timeout`
- `connection_failed`

### Ollama-statusar

- `reachable`
- `unreachable`
- `model_missing`

### HTTP-statuskoder

| HTTP  | Betydelse                              |
| ----- | -------------------------------------- |
| `200` | Alla komponenter fungerar              |
| `503` | En eller flera komponenter har problem |

## Kodkvalitet

Projektet använder Ruff för kontroll av Python-kod.

Kontrollera hela projektet:

```bash
python -m ruff check .
```

Automatisk korrigering av tillämpliga problem:

```bash
python -m ruff check . --fix
```

## Manuella tester

Databasanslutning:

```bash
python python/tests/test_connection.py
```

Ollama-anslutning och AI-generering:

```bash
python python/tests/test_ollama.py
```

Health Check:

```powershell
curl.exe -i http://127.0.0.1:5000/health
```

## Utvecklingsinformation

Projektet utvecklas stegvis med separata Git-branches och GitHub Issues.

Nya funktioner ska testas lokalt innan de mergas till huvudbranchen.
