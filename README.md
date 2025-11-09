# Roblox Friends Lookup

This simple Flask application lets you enter a Roblox user ID and view the user's friends using the public Roblox API.

## Prerequisites

- Python 3.10+
- pip

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
pip install -r requirements.txt
```

## Running the app

```bash
flask --app app run --debug
```

Then open http://127.0.0.1:5000/ in your browser, enter a Roblox user ID, and press **Search** to view their friends in a table with profile links and online status.

For production deployments (such as on Render), run the app with Gunicorn:

```bash
gunicorn app:app
```

