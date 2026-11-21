import os
from flask import Flask, redirect, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")
SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

def get_auth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".cache",
        show_dialog=True
    )

@app.route("/")
def home():
    return "Robot de Spotify activo - El tiempo es ORO, mi tiempo!"

@app.route("/login")
def login():
    auth = get_auth()
    return redirect(auth.get_authorize_url())

@app.route("/callback")
def callback():
    auth = get_auth()
    code = request.args.get("code")
    token_info = auth.get_access_token(code)
    return "Conectado con Spotify! Ya puedes cerrar esta ventana."

@app.route("/status")
def status():
    try:
        auth = get_auth()
        token_info = auth.get_cached_token()
        if not token_info:
            return jsonify({"status": "no_conectado", "mensaje": "Ve a /login primero"})
        sp = spotipy.Spotify(auth_manager=auth)
        current = sp.current_playback()
        return jsonify({"status": "conectado", "reproduciendo": current})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
