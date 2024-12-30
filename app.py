from flask import Flask, render_template, jsonify, send_from_directory
import os
import urllib.parse

app = Flask(__name__)

# Path to the music directory
MUSIC_DIR = '/media/gamedisk/Users/alp/Music'

# Function to get all supported audio files in the music directory
def get_audio_files():
    audio_extensions = ['.mp3', '.wav', '.flac', '.ogg']  # You can add more if needed
    audio_files = []
    
    for root, _, files in os.walk(MUSIC_DIR):
        for file in files:
            if any(file.endswith(ext) for ext in audio_extensions):
                # Use relative paths and encode spaces
                encoded_file = urllib.parse.quote(os.path.relpath(os.path.join(root, file), MUSIC_DIR))
                audio_files.append(encoded_file)
    
    return audio_files

# Initialize variables
songs = get_audio_files()  # Get list of all songs in the directory
current_song = None
is_playing = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control/<action>')
def control(action):
    global current_song, is_playing

    if action == 'play':
        if not current_song and songs:
            current_song = songs[0]  # Select the first song by default
        is_playing = True
        return jsonify({"status": f"Playing {current_song}"})

    elif action == 'pause':
        is_playing = False
        return jsonify({"status": f"Paused {current_song}"})

    elif action == 'resume':
        is_playing = True
        return jsonify({"status": f"Resumed {current_song}"})

    return jsonify({"status": "Action not recognized"})

@app.route('/search/<query>')
def search(query):
    matching_songs = [song for song in songs if query.lower() in song.lower()]
    return jsonify({"songs": matching_songs})

# Route to serve the audio files
@app.route('/music/<path:filename>')
def serve_music(filename):
    return send_from_directory(MUSIC_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)

