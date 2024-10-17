from flask import Flask, request, send_file, jsonify
from pathlib import Path
from translation.wisper import speach_to_text, text_to_speach
from translation.gpt import translate_text

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text")
    source_lang = data.get("source_lang")
    target_lang = data.get("target_lang")

    translated_text = translate_text(text, source_lang, target_lang)
    return jsonify({"translated_text": translated_text})

@app.route('/translate_audio', methods=['POST'])
def translate_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    source_lang = request.form.get('source_lang', 'en')
    target_lang = request.form.get('target_lang', 'ro')

    audio_file_path = Path("uploaded_audio.mp3")
    file.save(audio_file_path)
    text = speach_to_text(audio_file_path)
    translated_text = translate_text(text, source_lang, target_lang)
    speech_file_path = text_to_speach(translated_text)

    # Return the translated audio file to the user
    return send_file(speech_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)