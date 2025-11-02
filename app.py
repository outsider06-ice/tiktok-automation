from flask import Flask, request, jsonify
import json
import traceback

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Essaye d'abord le JSON standard
        if request.is_json:
            data = request.get_json()
        else:
            # Si échec, parse manuellement les données brutes
            raw_data = request.get_data(as_text=True)
            print("Raw data (potentiellement mal formé):", raw_data)
            
            # Nettoie et parse manuellement
            try:
                # Essaye de parser comme JSON
                data = json.loads(raw_data)
            except:
                # Fallback: traite comme texte simple
                data = {"script": raw_data.replace('"', '\\"')}
        
        script_content = data.get('script', '')
        print("Script reçu:", script_content)
        
        return jsonify({
            "status": "success",
            "message": "Script traité!",
            "script_length": len(script_content)
        })
        
    except Exception as e:
        print("ERREUR:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500
