from flask import Flask, jsonify

# Initialisation de l'application Flask
app = Flask(__name__)

@app.route('/api/v1/pronostics/today', methods=['GET'])
def get_today_pronostics():
    """
    Endpoint de test minimaliste. Si cette API répond, 
    cela prouve que le Procfile et la configuration de Render sont corrects.
    """
    return jsonify({
        "status": "success",
        "message": "API de DEBOGAGE en LIGNE. Le serveur Gunicorn démarre correctement.",
        "predictions": [] 
    })

# NOTE: La partie 'if __name__ == '__main__': ...' n'est pas nécessaire pour Render, 
# car Gunicorn démarre l'application directement via le Procfile.
