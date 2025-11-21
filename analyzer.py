import pandas as pd
from datetime import datetime
import os
import random

# --- Constantes ---
MIN_SOURCES_FOR_COUP_SUR = 12 
TOTAL_SOURCES = 20           

def analyze_raw_data(raw_data_filepath):
    """Charge les données, calcule le consensus et ajoute l'heure du match."""
    
    # 1. Gestion sécurisée du chemin de fichier pour Render
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(BASE_DIR, raw_data_filepath)
    
    try:
        df_raw = pd.read_csv(full_path)
        print(f"\n--- 1. Données brutes chargées : {len(df_raw)} entrées ---")
    except FileNotFoundError:
        print(f"Erreur: Fichier introuvable à {full_path}")
        return pd.DataFrame()
    
    prediction_types = [
        {'col_pred': 'raw_prediction_1X2', 'type': '1X2'},
        {'col_pred': 'raw_prediction_BTTS', 'type': 'BTTS (Les deux équipes marquent)'},
        {'col_pred': 'raw_prediction_OU25', 'type': 'Total Plus/Moins de 2.5'},
        {'col_pred': 'raw_prediction_YCards', 'type': 'Total Cartons Jaunes'}, 
        {'col_pred': 'raw_prediction_RBTT', 'type': 'Résultat + BTTS (Combiné)'},
    ]
    
    all_consensus_results = []
    
    # --- SIMULATION DE L'HEURE DU MATCH ---
    unique_match_ids = df_raw['match_id'].unique()
    match_time_map = {}
    
    for m_id in unique_match_ids:
        # Génère une heure aléatoire
        h = random.randint(14, 22)
        m = random.choice(['00', '15', '30', '45'])
        match_time_map[m_id] = f"{h}:{m}"

    for p_type in prediction_types:
        # Compter les votes
        if p_type['col_pred'] not in df_raw.columns:
            continue # Ignorer si la colonne n'existe pas dans le CSV

        consensus_df = df_raw.groupby(['match_id', 'home_team', 'away_team', p_type['col_pred']]).size().reset_index(name='vote_count')
        consensus_df['prediction_type'] = p_type['type']
        
        # Filtrer les Coups Sûrs
        df_coups_surs = consensus_df[consensus_df['vote_count'] >= MIN_SOURCES_FOR_COUP_SUR].copy()
        
        if not df_coups_surs.empty:
            df_coups_surs.rename(columns={p_type['col_pred']: 'raw_prediction'}, inplace=True)
            df_coups_surs['is_coup_sur'] = True
            df_coups_surs['total_sources'] = TOTAL_SOURCES
            df_coups_surs['match_time'] = df_coups_surs['match_id'].map(match_time_map)
            
            all_consensus_results.append(df_coups_surs)
            
    if not all_consensus_results:
        return pd.DataFrame()
        
    df_final = pd.concat(all_consensus_results, ignore_index=True)
    return df_final[['match_id', 'home_team', 'away_team', 'raw_prediction', 'vote_count', 'total_sources', 'is_coup_sur', 'prediction_type', 'match_time']]
