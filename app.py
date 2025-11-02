from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        raw_data = request.get_data(as_text=True)
        print("🔧 Données brutes reçues:", raw_data[:1000])

        # 1️⃣ Tentative JSON classique
        data = request.get_json(force=True, silent=True)
        if data and "script" in data:
            script_content = data["script"]
            method = "json"
        else:
            # 2️⃣ Tentative regex robuste
            match = re.search(r'"script"\s*:\s*"((?:\\.|[^"\\])*)"', raw_data)
            if match:
                script_content = match.group(1).replace('\\"', '"')
                method = "regex"
            else:
                script_content = "Script non trouvé"
                method = "fallback"

        print(f"✅ Script extrait via {method}: {len(script_content)} caractères")

        return jsonify({
            "status": "success",
            "method": method,
            "script_length": len(script_content),
            "preview": script_content[:100],
        })

    except Exception as e:
        return jsonify({
            "status": "repaired",
            "message": str(e),
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

