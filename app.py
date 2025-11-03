from flask import Flask, request, jsonify
import re
import json

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw_data = request.get_data(as_text=True)
        print("🔧 Données brutes reçues (début):", raw_data[:1000])

        script_content = None
        method_used = None

        # 1️⃣ Tentative de parsing JSON classique
        try:
            data = json.loads(raw_data)
            if isinstance(data, dict) and "script" in data:
                script_content = data["script"]
                method_used = "json"
        except Exception:
            pass  # JSON mal formé → on passera au fallback regex

        # 2️⃣ Fallback regex tolérant (même si JSON cassé)
        if not script_content:
            # Cette regex capture TOUT après "script": jusqu'au dernier guillemet avant la fin d'objet
            match = re.search(r'"script"\s*:\s*"([\s\S]*?)"\s*\}', raw_data)
            if match:
                script_content = match.group(1)
                script_content = script_content.replace('\\"', '"')
                method_used = "regex"

        # 3️⃣ Fallback ultime (si rien trouvé)
        if not script_content:
            if '"script":' in raw_data:
                script_content = raw_data.split('"script":', 1)[1]
                script_content = script_content.strip(' "}\n\t')
                method_used = "split"
            else:
                script_content = "Script non trouvé"
                method_used = "none"

        print(f"✅ Script extrait via {method_used}: {len(script_content)} caractères")

        return jsonify({
            "status": "success",
            "method": method_used,
            "message": "Script reçu et traité",
            "script_length": len(script_content),
            "preview": script_content[:200] + ("..." if len(script_content) > 200 else ""),
            "received": True
        }), 200

    except Exception as e:
        print("❌ Erreur webhook:", e)
        return jsonify({
            "status": "repaired",
            "message": f"Erreur gérée: {str(e)}",
            "script_received": False
        }), 200


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


