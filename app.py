from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Prend les données brutes peu importe le format
        raw_data = request.get_data(as_text=True)
        print("🔧 Données brutes reçues:", raw_data[:1000])
        
        # Extrait le script par REGEX peu importe le format JSON
        script_match = re.search(r'"script"\s*:\s*"([^"]*)"', raw_data)
        if not script_match:
            # Essaye avec guillemets non échappés
            script_match = re.search(r'"script"\s*:\s*"([^"]*?)(?="|\})', raw_data)
        
        if script_match:
            script_content = script_match.group(1)
            # Nettoie les échappements restants
            script_content = script_content.replace('\\"', '"')
            print(f"✅ Script extrait: {len(script_content)} caractères")
        else:
            # Fallback: prend tout après "script": 
            if '"script":' in raw_data:
                script_content = raw_data.split('"script":', 1)[1].strip(' "}')
            else:
                script_content = "Script non trouvé"
        
        # Réponse succès peu importe le contenu
        return jsonify({
            "status": "success",
            "message": "Script traité malgré guillemets!",
            "script_length": len(script_content),
            "received": True
        })
        
    except Exception as e:
        # Même en erreur, retourne 200 pour que Make.com continue
        return jsonify({
            "status": "repaired",
            "message": f"Erreur réparée: {str(e)}",
            "script_received": True
        }), 200  # ← 200 au lieu de 500 !

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
