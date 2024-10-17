from flask import Flask, request, jsonify
from flask_cors import CORS
from translation.mbard import MBartTranslator

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Initialize the MBartTranslator class
translator = MBartTranslator()

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    
    if not text or not source_lang or not target_lang:
        return jsonify({"error":"Missing text, source_lang, or target_lang"}),400

    # Use the MBartTranslator class to translate
    translated_text = translator.translate(text, source_lang, target_lang)
    
    return jsonify({"translated_text": translated_text})

@app.route('/languages', methods=['GET'])
def get_languages():
    # Get the list of supported languages
    languages = translator.get_supported_languages()
    
    # Format the languages into a JSON object (e.g., [{"code": "en_XX", "name": "English"}, ...])
    language_names = {
        "en_XX": "English",
        "fr_XX": "French",
        "es_XX": "Spanish",
        "de_DE": "German",
        "it_IT": "Italian",
        "pt_XX": "Portuguese",
        "ru_RU": "Russian",
        "zh_CN": "Chinese",
        "ja_XX": "Japanese",
        "ko_KR": "Korean",
        "ro_RO": "Romanian",
        # Add more language names if needed
    }

    # Construct list of dictionaries with language code and name
    languages_list = [{"code": lang, "name": language_names[lang]} for lang in languages if lang in language_names]
   
    return jsonify({"languages": languages_list})

if __name__ == '__main__':
    app.run(debug=True)
