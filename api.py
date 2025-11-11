from flask import Flask, jsonify
from datetime import datetime
import os
import pandas as pd # NOUVEL IMPORT NÉCESSAIRE

# Nous allons importer la logique de calcul depuis analyzer.py
# (Si vous avez renommé analyzer.py en analyseur.py, changez le nom ici)
from analyzer import analyze_raw_data 

app = Flask(__name__)

# --- Fonction qui lit les données (utilise pandas) ---
def get_latest_results():
    """Charge et prépare les derniers résultats consolidés en JSON."""
    
    # Render exécute le code à la racine. __file__ est le chemin de api.py.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    all_files = os.listdir(BASE_DIR)
    
    # 1. Trouver le dernier fichier consolidé (assurez-vous d'avoir ce fichier sur GitHub)
    result_files = [f for f in all_files if f.startswith('consolidated_results_') and f.endswith('.csv')]
    
    if not result_files:
        # Tente de générer les données si elles ne sont pas trouvées (méthode de débogage)
        print("Alerte: Aucun fichier consolidé trouvé. L'API renvoie des données vides.")
        return []

    latest_file = max(result_files)
    latest_filepath = os.path.join(BASE_DIR, latest_file) # Utilise le chemin absolu

    try:
        # Lire le fichier CSV avec Pandas
        df_results = pd.read_csv(latest_filepath)
        
        # SÉLECTION DES COLONNES NÉCESSAIRES (comme dans les anciennes versions)
        df_results = df_results[[
            'match_id', 'home_team', 'away_team', 'raw_prediction',
            'vote_count', 'total_sources', 'is_coup_sur', 'prediction_type',
            'match_time' 
        ]].copy()
        
        df_results = df_results.fillna('') 
        return df_results.to_dict(orient='records')
    
    except Exception as e:
        print(f"Erreur fatale lors de la lecture des CSV: {e}")
        return []

@app.route('/api/v1/pronostics/today', methods=['GET'])
def get_today_pronostics():
    """Endpoint qui retourne la liste des Coups Sûrs du jour."""
    
    # 🚨 NOTE: L'analyse des CSV est maintenant déplacée dans la fonction get_latest_results()
    results = get_latest_results()
    
    if not results:
        # Si la fonction get_latest_results() échoue ou renvoie []
        return jsonify({
            "status": "success", 
            "message": "API en ligne, mais aucun pronostic trouvé (CSV vide ou lecture échouée).",
            "predictions": []
        }), 200 # Retourne 200 (Succès) même si les prédictions sont vides
    
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "count": len(results),
        "predictions": results
    })

# Le Procfile lance Gunicorn, donc ce bloc n'est pas utilisé.
# if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=5000)
