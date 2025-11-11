# api.py

from flask import Flask, jsonify
import pandas as pd
import os
import json
from datetime import datetime

app = Flask(__name__)

def get_latest_results():
    """Charge et prépare les derniers résultats consolidés en JSON."""
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    all_files = os.listdir(backend_dir)
    
    result_files = [f for f in all_files if f.startswith('consolidated_results_') and f.endswith('.csv')]
    
    if not result_files:
        return []

    latest_file = max(result_files)
    latest_filepath = os.path.join(backend_dir, latest_file)
    
    df_results = pd.read_csv(latest_filepath)

    # Colonnes finales pour l'API
    df_results = df_results[[
        'match_id', 
        'home_team', 
        'away_team', 
        'raw_prediction',
        'vote_count',
        'total_sources',
        'is_coup_sur',
        'prediction_type'
    ]].copy()
    
    df_results = df_results.fillna('') 
    
    return df_results.to_dict(orient='records')

@app.route('/api/v1/pronostics/today', methods=['GET'])
def get_today_pronostics():
    """Endpoint qui retourne la liste des Coups Sûrs du jour."""
    
    results = get_latest_results()
    
    if not results:
        return jsonify({
            "status": "error",
            "message": "Aucun pronostic disponible. Le moteur d'analyse est en cours d'exécution."
        }), 503
    
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "count": len(results),
        "predictions": results
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)