from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # 🔧 Récupère les données brutes
        raw_data = request.get_data(as_text=True)
        print("🔧 Données brutes reçues (début):", raw_data[:1000])

        # 🧩 Étape 1 : tentative de parsing JSON propre
        data = request.get_json(force=True, silent=True)
        script_content = None
        method_used = None

        if data and "script" in data:
            # ✅ Cas normal : Make.com envoie un JSON bien formé
            script_content = data["script"]
            method_used = "json"
        else:
            # 🧩 Étape 2 : fallback via REGEX robuste
            match = re.search(r'"script"\s*:\s*"((?:\\.|[^"\\])*)"', raw_data, re.S)
            if match:
                script_content = match.group(1).replace('\\"', '"')
                method_used = "regex"
            else:
                # 🧩 Étape 3 : fallback ultime (tentative de découpe simple)
                if '"script":' in raw_data:
                    script_content = raw_data.split('"script":', 1)[1].split("}", 1)[0]
                    script_content = script_content.strip(' "}\n\t')
                    method_used = "split"
                else:
                    script_content = "Script non trouvé"
                    method_used = "none"

        print(f"✅ Script extrait via {method_used}: {len(script_content)} caractères")

        # ✅ Réponse JSON pour Make.com
        return jsonify({
            "status": "success",
            "method": method_used,
            "message": "Script reçu et traité",
            "script_length": len(script_content),
            "preview": script_content[:150] + ("..." if len(script_content) > 150 else ""),
            "received": True
        }), 200

    except Exception as e:
        # 🔁 Toujours renvoyer 200 pour éviter que Make échoue
        print("❌ Erreur webhook:", e)
        return jsonify({
            "status": "repaired",
            "message": f"Erreur gérée: {str(e)}",
            "script_received": False
        }), 200

# 🔓 (Optionnel) Autoriser les requêtes cross-origin
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

