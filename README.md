# Live Chat Audio Translation App

This Flask-based app allows for real-time audio message translation using OpenAI’s ChatGPT for text translation and Firebase for storing and retrieving audio files.

## Features

- **Audio Translations**: Converts speech-to-text, translates it, and returns text-to-speech in the target language.
- **Firebase Integration**: Audio files are uploaded and retrieved from Firebase Storage.
- **Multi-user Chat**: Support for translating and storing audio messages between different users.

## Prerequisites

- **Python 3.8+**
- **Firebase Project** with Storage enabled
- **OpenAI API Key** (for ChatGPT model translations)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/adelen99/RebelDot.git
cd RebelDot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Firebase Configuration

Go to the Firebase Console and download the Firebase Admin SDK JSON credentials from Project Settings > Service Accounts.
Place the firebase-adminsdk.json file in the root directory of your project.

### 4. Environment Variables

```bash
FIREBASE_CREDENTIALS=path/to/firebase-adminsdk.json
FIREBASE_BUCKET=your-project-id.appspot.com
OPEN_AI_KEY=your-openai-api-key
```

### 5. Run the Application

```bash
npm run dev
python -m main
```

 
