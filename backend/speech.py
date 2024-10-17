from flask import Flask, request, send_file, jsonify
from pathlib import Path
from translation.wisper import speach_to_text, text_to_speach

app = Flask(__name__)

@app.route('/translate_audio', methods=['POST'])
def translate_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    audio_file_path = Path("uploaded_audio.mp3")
    file.save(audio_file_path)
    text = speach_to_text(audio_file_path)
    speech_file_path = text_to_speach(text)

    # Return the translated audio file to the user
    return send_file(speech_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)