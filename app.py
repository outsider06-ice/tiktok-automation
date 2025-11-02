from flask import Flask, request, jsonify
import traceback
import sys

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Force l'affichage dans les logs Render
        print("=== DÉBUT WEBHOOK ===", file=sys.stderr)
        print(f"Method: {request.method}", file=sys.stderr)
        print(f"Content-Type: {request.content_type}", file=sys.stderr)
        
        # Essaye de lire les données
        if request.is_json:
            data = request.get_json()
            print(f"JSON data: {data}", file=sys.stderr)
        else:
            raw_data = request.get_data(as_text=True)
            print(f"Raw data: {raw_data}", file=sys.stderr)
            data = None
        
        # Réponse SIMPLE pour tester
        response = {
            "status": "success", 
            "message": "Test réussi depuis Render!",
            "data_received": data if data else "No data"
        }
        
        print("=== RÉPONSE ENVOYÉE ===", file=sys.stderr)
        return jsonify(response)
        
    except Exception as e:
        # Log l'erreur COMPLÈTE
        error_trace = traceback.format_exc()
        print(f"=== ERREUR DÉTAILLÉE ===\n{error_trace}", file=sys.stderr)
        
        return jsonify({
            "error": str(e),
            "traceback": error_trace
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Service actif!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
