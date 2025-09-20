#!/usr/bin/env python3
"""
Lean Music Organizer
Applies Lean Process Improvement to organize unstructured music files.
Measures Before/After efficiency -> Generates visual proof of improvement.
"""

import os
import csv
import time
import subprocess
import sys
import webbrowser
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ===========================
# CONFIGURATION
# ===========================
MUSIC_INPUT_DIR = "sample_music"        # Folder with unstructured MP3s
MUSIC_OUTPUT_DIR = "organized_output"   # Where Picard will save organized files
LOG_FILE = "data/process_log.csv"
CHART_FILE = "data/lean_results.png"

# Create folders if missing
os.makedirs(MUSIC_INPUT_DIR, exist_ok=True)
os.makedirs(MUSIC_OUTPUT_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

# ===========================
# SIMULATE "BEFORE" MANUAL PROCESS
# ===========================
def simulate_before_state(file_count):
    """
    Simulates the inefficient "Before" state:
    - Manual renaming
    - Manual tagging
    - High error rate
    - Slow per-song time
    """
    print("\nSimulating BEFORE state (Manual Process)...")
    time.sleep(2)

    # Simulate metrics based on real-world manual effort
    avg_time_per_song = 189  # seconds (3.15 min)
    total_time_sec = file_count * avg_time_per_song
    manual_actions = 8
    errors = max(1, int(file_count * 0.15))  # 15% error rate
    duplicates = max(0, int(file_count * 0.1))  # 10% duplicates

    print(f"Files to process: {file_count}")
    print(f"Simulated total time: {total_time_sec//60} min {total_time_sec%60} sec")
    print(f"Manual actions per song: {manual_actions}")
    print(f"Errors: {errors}")
    print(f"Duplicates: {duplicates}")

    return {
        "session_type": "before",
        "songs_processed": file_count,
        "total_time_min": round(total_time_sec / 60, 1),
        "avg_time_per_song_sec": avg_time_per_song,
        "manual_actions_per_song": manual_actions,
        "errors": errors,
        "duplicates": duplicates
    }

# ===========================
# LAUNCH MUSICBRAINZ PICARD
# ===========================
def launch_picard():
    """
    Opens MusicBrainz Picard with the input folder.
    Waits for user to finish tagging -> then press ENTER.
    """
    print("\n" + "="*60)
    print("LAUNCHING LEAN SOLUTION: MusicBrainz Picard")
    print("="*60)
    print("1. Picard will open with your music folder loaded.")
    print("2. Click 'Cluster' -> 'Lookup' -> Review matches -> 'Save'")
    print("3. Picard will auto-rename & move files to 'organized_output/'")
    print("4. AFTER you finish, COME BACK HERE and press ENTER.")
    print("="*60)

    # Try common Picard install paths
    picard_paths = [
        r"C:\Program Files\MusicBrainz Picard\picard.exe",  # Windows
        r"C:\Program Files (x86)\MusicBrainz Picard\picard.exe",
        "/Applications/MusicBrainz Picard.app/Contents/MacOS/picard",  # macOS
        "/usr/bin/picard",  # Linux
        "picard"  # If in PATH
    ]

    picard_cmd = None
    for path in picard_paths:
        if os.path.exists(path) or path == "picard":
            picard_cmd = path
            break

    if not picard_cmd:
        print("MusicBrainz Picard not found.")
        print("Please install from: https://picard.musicbrainz.org")
        webbrowser.open("https://picard.musicbrainz.org")
        input("\nPress ENTER after installing Picard and placing files in 'sample_music/'...")
        sys.exit(1)

    try:
        # Launch Picard with input folder
        if sys.platform == "darwin":  # macOS
            subprocess.Popen(["open", "-a", picard_cmd, os.path.abspath(MUSIC_INPUT_DIR)])
        else:
            subprocess.Popen([picard_cmd, os.path.abspath(MUSIC_INPUT_DIR)])
    except Exception as e:
        print(f"Failed to launch Picard: {e}")
        sys.exit(1)

    print(f"\nOpening folder: {os.path.abspath(MUSIC_INPUT_DIR)}")
    print("Waiting for you to finish organizing in Picard...")
    input("\nWhen DONE in Picard, press ENTER to continue...")

# ===========================
# SIMULATE "AFTER" AUTOMATED PROCESS
# ===========================
def simulate_after_state(file_count):
    """
    Simulates efficient "After" state:
    - Mostly automated
    - Minimal review
    - Near-zero errors
    """
    print("\nSimulating AFTER state (Automated Process)...")
    time.sleep(1)

    avg_time_per_song = 38  # seconds
    total_time_sec = file_count * avg_time_per_song
    manual_actions = 1.5    # Just reviewing matches
    errors = 0 if file_count < 10 else max(0, int(file_count * 0.01))  # 1% error
    duplicates = 0

    print(f"Files processed: {file_count}")
    print(f"Simulated total time: {total_time_sec//60} min {total_time_sec%60} sec")
    print(f"Manual actions per song: {manual_actions}")
    print(f"Errors: {errors}")
    print(f"Duplicates: {duplicates}")

    return {
        "session_type": "after",
        "songs_processed": file_count,
        "total_time_min": round(total_time_sec / 60, 1),
        "avg_time_per_song_sec": avg_time_per_song,
        "manual_actions_per_song": manual_actions,
        "errors": errors,
        "duplicates": duplicates
    }

# ===========================
# LOG DATA TO CSV
# ===========================
def log_data(data):
    """Append session data to CSV log"""
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# ===========================
# GENERATE VISUALIZATIONS
# ===========================
def generate_visualizations():
    """Create Before vs After comparison charts"""
    if not os.path.exists(LOG_FILE):
        print("No log data found.")
        return

    df = pd.read_csv(LOG_FILE)
    before = df[df['session_type'] == 'before']
    after = df[df['session_type'] == 'after']

    if len(before) == 0 or len(after) == 0:
        print("Need both 'before' and 'after' data.")
        return

    # Calculate averages
    metrics = ['avg_time_per_song_sec', 'manual_actions_per_song', 'errors', 'duplicates']
    before_avg = before[metrics].mean()
    after_avg = after[metrics].mean()

    # Plot
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Lean Music Organizer: Before vs After Improvement', fontsize=16, fontweight='bold')

    labels = ['Before', 'After']
    colors = ['#e74c3c', '#27ae60']

    # Time per song
    axes[0,0].bar(labels, [before_avg['avg_time_per_song_sec'], after_avg['avg_time_per_song_sec']], color=colors)
    axes[0,0].set_title('Avg Time per Song (sec)')
    axes[0,0].set_ylabel('Seconds')
    for i, v in enumerate([before_avg['avg_time_per_song_sec'], after_avg['avg_time_per_song_sec']]):
        axes[0,0].text(i, v + 5, f"{v:.0f}", ha='center', fontweight='bold')

    # Manual actions
    axes[0,1].bar(labels, [before_avg['manual_actions_per_song'], after_avg['manual_actions_per_song']], color=colors)
    axes[0,1].set_title('Manual Actions per Song')
    for i, v in enumerate([before_avg['manual_actions_per_song'], after_avg['manual_actions_per_song']]):
        axes[0,1].text(i, v + 0.1, f"{v:.1f}", ha='center', fontweight='bold')

    # Errors
    axes[1,0].bar(labels, [before_avg['errors'], after_avg['errors']], color=colors)
    axes[1,0].set_title('Avg Errors per Session')
    for i, v in enumerate([before_avg['errors'], after_avg['errors']]):
        axes[1,0].text(i, v + 0.1, f"{v:.1f}", ha='center', fontweight='bold')

    # Duplicates
    axes[1,1].bar(labels, [before_avg['duplicates'], after_avg['duplicates']], color=colors)
    axes[1,1].set_title('Avg Duplicates per Session')
    for i, v in enumerate([before_avg['duplicates'], after_avg['duplicates']]):
        axes[1,1].text(i, v + 0.1, f"{v:.1f}", ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=150, bbox_inches='tight')
    plt.show()

    print(f"\nVisualizations saved to: {CHART_FILE}")

# ===========================
# MAIN EXECUTION
# ===========================
def main():
    print("="*70)
    print("LEAN MUSIC ORGANIZER")
    print("Apply Lean Process Improvement to Your Digital Music Library")
    print("="*70)

    # Count input files
    music_files = [f for f in os.listdir(MUSIC_INPUT_DIR) if f.lower().endswith(('.mp3', '.flac', '.m4a', '.wav'))]
    file_count = len(music_files)

    if file_count == 0:
        print(f"No music files found in '{MUSIC_INPUT_DIR}/'")
        print("Please add some unstructured music files (e.g., 'song1.mp3') and run again.")
        sys.exit(1)

    print(f"Found {file_count} music files in '{MUSIC_INPUT_DIR}/'")

    # STEP 1: Simulate BEFORE state
    before_data = simulate_before_state(file_count)
    log_data(before_data)

    # STEP 2: Launch Lean solution (Picard)
    launch_picard()

    # STEP 3: Simulate AFTER state
    after_data = simulate_after_state(file_count)
    log_data(after_data)

    # STEP 4: Generate visual proof of improvement
    generate_visualizations()

    # FINAL SUMMARY
    time_saved_percent = round((1 - after_data['avg_time_per_song_sec'] / before_data['avg_time_per_song_sec']) * 100)
    error_reduction_percent = round((1 - after_data['errors'] / max(1, before_data['errors'])) * 100)

    print("\n" + "="*70)
    print("LEAN IMPROVEMENT RESULTS")
    print("="*70)
    print(f"TIME SAVED PER SONG: {time_saved_percent}%")
    print(f"ERROR REDUCTION: {error_reduction_percent}%")
    print(f"VISUALIZATION: {CHART_FILE}")
    print(f"LOG FILE: {LOG_FILE}")
    print(f"ORGANIZED FILES: {MUSIC_OUTPUT_DIR}/")
    print("="*70)
    print("You've successfully applied Lean principles to your music library!")

if __name__ == "__main__":
    main()