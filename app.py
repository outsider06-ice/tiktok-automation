from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("✅ Données reçues :", data)
        
        # Traitement du script TikTok
        script_content = data.get('script', '')
        
        # Ici tu peux ajouter ton traitement
        response_data = {
            "status": "success",
            "message": "Script TikTok traité avec Render!",
            "script_received": script_content,
            "source": "render.com"
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print("❌ Erreur :", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "tiktok-automation"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
