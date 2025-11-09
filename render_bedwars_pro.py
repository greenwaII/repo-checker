"""BedWars montage renderer helper script.

Analyzes the audio track to detect beats and invokes FFmpeg with a
preconfigured filter script. This version ensures the generated video
and audio streams from the filter graph are explicitly mapped so FFmpeg
no longer reports unconnected outputs.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import librosa
import numpy as np

CURRENT_DIR = Path(__file__).resolve().parent
VIDEO_PATH = CURRENT_DIR / "gameplay.mp4"
AUDIO_PATH = CURRENT_DIR / "audio.mp3"
FILTERS_PATH = CURRENT_DIR / "filters_pro.txt"
OUTPUT_PATH = CURRENT_DIR / "bedwars_montage_pro.mp4"


def _require(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"❌ Required file not found: {path}")


def analyze_beats(audio_path: Path) -> tuple[float, np.ndarray]:
    y, sr = librosa.load(audio_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    return float(tempo), beats


def build_command() -> list[str]:
    """Construct the FFmpeg command with explicit stream mappings."""
    return [
        "ffmpeg",
        "-y",
        "-i",
        str(VIDEO_PATH),
        "-i",
        str(AUDIO_PATH),
        "-filter_complex_script",
        str(FILTERS_PATH),
        "-map",
        "[vout]",
        "-map",
        "[aout]",
        "-shortest",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(OUTPUT_PATH),
    ]


def main() -> None:
    print("🎵 Analyzing beats...")

    _require(VIDEO_PATH)
    _require(AUDIO_PATH)
    _require(FILTERS_PATH)

    tempo, beats = analyze_beats(AUDIO_PATH)
    print(f"Detected {len(beats)} beats at {tempo:.1f} BPM")
    print(f"✅ Using filters file: {FILTERS_PATH}\n")

    command = build_command()
    print("⚙️ Running FFmpeg command:")
    print(" ".join(command))

    try:
        result = subprocess.run(command, check=False)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "FFmpeg executable not found. Make sure it is installed and on your PATH."
        ) from exc

    if result.returncode == 0:
        print(f"✅ Render complete! Saved as: {OUTPUT_PATH}")
    else:
        print("❌ FFmpeg failed. Please check your filters_pro.txt formatting.")


if __name__ == "__main__":
    main()
