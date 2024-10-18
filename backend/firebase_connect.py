import requests
import firebase_admin
from firebase_admin import credentials, storage, firestore

# Înlocuiește "path/to/firebase-adminsdk.json" cu calea către fișierul tău JSON
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(
    cred, {"storageBucket": "react-livechat-ff02b.appspot.com"}
)

# Acum ai acces la Firebase Storage
bucket = storage.bucket()

db = firestore.client()


def upload_audio_to_firebase(local_file_path, file_name):
    bucket = storage.bucket()

    # Specifică folderul `received_audios` pentru salvare
    blob = bucket.blob(f"received_audios/{file_name}")

    # Încarcă fișierul local în Storage
    blob.upload_from_filename(local_file_path)

    # Fă fișierul accesibil public, dacă este necesar
    blob.make_public()

    # Returnează URL-ul public al fișierului încărcat
    return blob.public_url


def download_audio_from_url(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        return save_path
    else:
        return None


def save_audio_metadata_to_firestore(
    audio_url, created_at, receiver_id, sender_id, text, translated_text, chat_id
):
    # Structura mesajului audio
    audio_message = {
        "audio": audio_url,
        "createdAt": created_at,
        "img": None,
        "receiverId": receiver_id,
        "senderId": sender_id,
        "text": text,
        "translatedText": translated_text,
    }

    # Referință la documentul cu chatId
    chat_doc_ref = db.collection("chats").document(chat_id)

    # Actualizează documentul pentru a adăuga mesajul audio în array-ul messages
    chat_doc_ref.update(
        {
            "messages": firestore.ArrayUnion(
                [audio_message]
            )  # Adaugă mesajul audio la array-ul messages
        }
    )
