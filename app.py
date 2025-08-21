from flask import Flask, request, jsonify, render_template
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os, sys

app = Flask(__name__)

# ---------------- Google Sheets ----------------
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

SERVICE_ACCOUNT_FILE = os.path.join(base_path, "felmeddelanden-bedc86615fa6.json")
SHEET_ID = "1jER2ZWJSJMzEMBdk_ovJgq3bc7sbg_tEuv3KnY9STfI"

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SHEET_ID).sheet1

# ---------------- Kategorier ----------------
kategorier = {
    "Kok": ["Lutkar", "Bläster", "Verktygsdelare", "Pallställage", "Trolley", "Övrigt"],
    "Press": ["Götlagring", "Götugn", "Shear", "Press", "Kylbox", "Runout", "Puller", "Pullersåg", "Verktygsugnar", "Övrigt"],
    "Sträck": ["Värmeband", "Huvudsträck", "Mothåll", "Övrigt"],
    "Korghantering": ["Tomkorgsstaplare", "Korgpositioner", "Övrigt"],
    "Kap": ["Transferbom", "Inmatningsrullar", "Kap", "Rullar efter kap", "Skrothantering", "Stacker", "Spacehantering", "Övrigt"],
    "IUT": ["Korgstaplare", "Transfervagn", "Ugn 1-4", "Kylstation", "Korgkran", "Övrigt"],
    "Destack": ["Spacehantering", "Destacker", "Korgpositioner", "Övrigt"],
    "Pack": ["Rullar", "Packbord 1-4", "Plastmaskin", "Övrigt"],
    "Byggnad": ["Läckage", "Påkörning", "Övrigt"]
    # fortsätt med resten av kategorierna
}

# ---------------- Routes ----------------
@app.route('/')
def index():
    return render_template('index.html', kategorier=kategorier)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    huvudkategori = data.get("huvudkategori")
    underkategori = data.get("underkategori")
    fritext = data.get("fritext")
    if fritext:
        tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([huvudkategori, underkategori, fritext, tid])
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
