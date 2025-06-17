from flask import Flask, jsonify, send_from_directory, render_template
import json
import os

app = Flask(__name__, static_folder = 'static')

# Percorsi per audio tagliati (statici) e interi (dinamici)
AUDIO_STATIC_DIR = os.path.join(app.root_path, 'static', 'audio')
AUDIO_DINAMICO_DIR = os.path.join(app.root_path, 'static', 'audio_non_tagliati')

try:
    with open(os.path.join(app.root_path, "static", "domande.json"), "r", encoding="utf-8") as f:
        domande = json.load(f)
except FileNotFoundError:
    print("Errore: Il file domande.json non è stato trovato nella cartella static/. Assicurati che esista.")
    domande = [] # Inizializza come lista vuota per evitare errori se il file manca

# Rotta principale per la pagina del consenso.
@app.route("/")
def consenso():
    # Renderizza il file HTML dalla cartella 'templates/'.
    return render_template("consenso.html")

# Rotta per la pagina del quiz (il sondaggio principale).
@app.route("/quiz")
def quiz():
    # Renderizza il file HTML dalla cartella 'templates/'.
    return render_template("index.html")

# Rotta per la pagina finale dopo aver completato il sondaggio.
@app.route("/fine")
def fine():
    # Renderizza il file HTML dalla cartella 'templates/'.
    return render_template("finale.html")

# Rotta per servire i file audio dalla cartella 'static/audio'.
# L'argomento 'static_folder' in Flask gestisce automaticamente questo.
# Questa rotta è più specifica per garantire che i file audio siano accessibili
# se ci fossero problemi con il serving automatico.
@app.route("/static/audio/<path:filename>")
def serve_audio_static(filename):
    return send_from_directory(AUDIO_STATIC_DIR, filename)

# Rotta per servire i file audio dalla cartella 'static/audio_tagliati'.
# Abbiamo corretto il nome della cartella qui per renderlo coerente con il frontend.
@app.route("/static/audio_tagliati/<path:filename>") # Corretto il nome della cartella qui
def serve_audio_dinamico(filename):
    return send_from_directory(AUDIO_DINAMICO_DIR, filename)

# Il blocco seguente assicura che l'applicazione venga eseguita solo
# quando lo script è avviato direttamente (e non quando importato come modulo).
# Questo è il blocco corretto per il deploy su Render (e test locale).
# Render utilizzerà la variabile d'ambiente 'PORT', altrimenti userà 5000.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=True)
