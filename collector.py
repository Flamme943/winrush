# collector.py (VERSION SIMULATION COMPLÈTE - PAS DE 'requests' nécessaire)

import pandas as pd
from datetime import datetime
import os
import time

def run_collector():
    
    # --- 1. Simulation des données brutes (5 types de pronostics) ---
    all_raw_data = []

    # Match A (Man City vs Arsenal) aura un Coup Sûr sur les 5 types
    match_id_A = "TEST_MATCH_20251109_A"
    
    # 20 sources au total
    data_match_A = [
        # 12 votes pour le consensus (V1, Yes, Over 2.5, Over 4.5, V1+Yes)
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"}, 
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"}, 
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"}, 
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"}, 
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"}, 
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"},
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"},
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"},
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"},
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"},
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"},
        {"pred_1X2": "1", "pred_BTTS": "Yes", "pred_OU25": "Over 2.5", "pred_YCards": "Over 4.5", "pred_RBTT": "V1+Yes"}, # 12ème vote

        # 8 votes pour la minorité/autres options (X, No, Under 2.5, Under 4.5, X+No)
        {"pred_1X2": "X", "pred_BTTS": "No", "pred_OU25": "Under 2.5", "pred_YCards": "Under 4.5", "pred_RBTT": "X+No"},
        {"pred_1X2": "X", "pred_BTTS": "No", "pred_OU25": "Under 2.5", "pred_YCards": "Under 4.5", "pred_RBTT": "X+No"},
        {"pred_1X2": "X", "pred_BTTS": "No", "pred_OU25": "Under 2.5", "pred_YCards": "Under 4.5", "pred_RBTT": "X+No"},
        {"pred_1X2": "X", "pred_BTTS": "No", "pred_OU25": "Under 2.5", "pred_YCards": "Under 4.5", "pred_RBTT": "X+No"},
        {"pred_1X2": "X", "pred_BTTS": "No", "pred_OU25": "Under 2.5", "pred_YCards": "Under 4.5", "pred_RBTT": "X+No"},
        {"pred_1X2": "X", "pred_BTTS": "No", "pred_OU25": "Under 2.5", "pred_YCards": "Under 4.5", "pred_RBTT": "X+No"},
        {"pred_1X2": "X", "pred_BTTS": "No", "pred_OU25": "Under 2.5", "pred_YCards": "Under 4.5", "pred_RBTT": "X+No"},
        {"pred_1X2": "X", "pred_BTTS": "No", "pred_OU25": "Under 2.5", "pred_YCards": "Under 4.5", "pred_RBTT": "X+No"}, # 8ème vote
    ]
    
    # Remplissage des données complètes pour toutes les 20 sources simulées
    for i, item in enumerate(data_match_A):
        all_raw_data.append({
            "match_id": match_id_A,
            "source_name": f"Source_{i+1}",
            "timestamp": datetime.now().isoformat(),
            "competition": "Premier League",
            "home_team": "Manchester City",
            "away_team": "Arsenal",
            
            # Type 1 : 1X2
            "raw_prediction_1X2": item["pred_1X2"],
            "raw_odd_1X2": 1.50 if item["pred_1X2"] == "1" else 3.50,
            
            # Type 2 : BTTS
            "raw_prediction_BTTS": item["pred_BTTS"],
            "raw_odd_BTTS": 1.70 if item["pred_BTTS"] == "Yes" else 2.10,
            
            # Type 3 : O/U 2.5
            "raw_prediction_OU25": item["pred_OU25"],
            "raw_odd_OU25": 1.80 if item["pred_OU25"] == "Over 2.5" else 2.00,

            # Type 4 : Cartons Jaunes (YCards)
            "raw_prediction_YCards": item["pred_YCards"],
            "raw_odd_YCards": 1.75 if item["pred_YCards"] == "Over 4.5" else 2.05, 
            
            # Type 5 : Résultat + BTTS (Combiné)
            "raw_prediction_RBTT": item["pred_RBTT"],
            "raw_odd_RBTT": 2.69 if item["pred_RBTT"] == "V1+Yes" else 5.35, 
            
            "source_reliability": 0.80 
        })
        
    # --- 2. Création et stockage du DataFrame ---
    df_raw = pd.DataFrame(all_raw_data)
    
    # Sauvegarde dans un fichier horodaté
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"raw_data_simulated_{timestamp_str}.csv"
    
    df_raw.to_csv(os.path.join(os.path.dirname(__file__), filename), index=False)
    
    print(f"\n--- Démarrage du Moteur WinRush : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    print(f"Succès: {len(df_raw)} entrées collectées et stockées.")
    
    print("\nAperçu des données brutes (Raw Data):")
    print(df_raw[['match_id', 'raw_prediction_1X2', 'raw_prediction_BTTS', 'raw_prediction_RBTT']].head())
    
    return filename

if __name__ == "__main__":
    run_collector()