from flask import Flask, request, jsonify
import json
import traceback

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        print("=== TENTATIVE DE RÉCEPTION ===")
        
        # Essaye d'abord le JSON standard
        if request.is_json:
            data = request.get_json()
            print("✅ JSON bien formé reçu")
        else:
            # Si échec, parse manuellement les données brutes
            raw_data = request.get_data(as_text=True)
            print("⚠️ Données brutes reçues:", raw_data[:500] + "..." if len(raw_data) > 500 else raw_data)
            
            # Nettoie et parse manuellement
            try:
                # Essaye de parser comme JSON
                data = json.loads(raw_data)
                print("✅ JSON réparé avec succès")
            except json.JSONDecodeError:
                # Si échec, cherche le script manuellement
                print("❌ JSON invalide, fallback manuel")
                if 'script' in raw_data:
                    # Extrait le script manuellement
                    start = raw_data.find('"script": "') + 11
                    end = raw_data.find('"', start)
                    script_content = raw_data[start:end] if start > 10 else "Script non trouvé"
                    data = {"script": script_content}
                else:
                    data = {"script": raw_data}
        
        script_content = data.get('script', '')
        print(f"📝 Script extrait ({len(script_content)} caractères):", script_content[:200] + "..." if len(script_content) > 200 else script_content)
        
        return jsonify({
            "status": "success",
            "message": "Script traité avec succès!",
            "script_length": len(script_content),
            "received_via": "render_corrected"
        })
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"💥 ERREUR CRITIQUE: {str(e)}")
        print(f"📋 TRACEBACK: {error_trace}")
        return jsonify({
            "error": str(e),
            "traceback": error_trace
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "version": "corrected"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
