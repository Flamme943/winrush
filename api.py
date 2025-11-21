from flask import Flask, jsonify
import pandas as pd
import os
from datetime import datetime
from analyzer import analyze_raw_data # Importe votre fonction d'analyse

app = Flask(__name__)

def get_latest_results():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        all_files = os.listdir(BASE_DIR)
        # Trouve le fichier raw_data le plus récent (les données brutes)
        raw_files = [f for f in all_files if f.startswith('raw_data_simulated_') and f.endswith('.csv')]
        
        if not raw_files:
            return []

        latest_file = max(raw_files)
        
        # Lance l'analyse en direct sur le fichier
        df_results = analyze_raw_data(latest_file)
        
        if df_results.empty:
            return []
            
        df_results = df_results.fillna('')
        return df_results.to_dict(orient='records')

    except Exception as e:
        print(f"Erreur API: {e}")
        return []

@app.route('/', methods=['GET'])
def home():
    return "API WinRush Active", 200

@app.route('/api/v1/pronostics/today', methods=['GET'])
def get_today_pronostics():
    results = get_latest_results()
    
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "count": len(results),
        "predictions": results
    })
