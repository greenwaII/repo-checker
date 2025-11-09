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

Then open http://127.0.0.1:5000/ in your browser, enter a Roblox user ID, and press **Search** to view their friends in a table.

## Rendering a BedWars montage (optional helper script)

The repository also contains `render_bedwars_pro.py`, a helper that analyzes an audio track for beats and then renders a montage using FFmpeg filters defined in `filters_pro.txt`.

1. Place `gameplay.mp4` and `audio.mp3` alongside the script (or edit the paths at the top of the file).
2. Ensure FFmpeg, NumPy, and Librosa are installed.
3. Run the renderer:

   ```bash
   python render_bedwars_pro.py
   ```

The script explicitly maps the filtered video (`[vout]`) and audio (`[aout]`) streams, preventing FFmpeg from failing with “Filter 'fade:default' has output 0 (vout) unconnected”.
