# analyzer.py

import pandas as pd
from datetime import datetime
import os
import random # Ajout pour simuler l'heure du match

# --- Définition des constantes de la règle WinRush ---
MIN_SOURCES_FOR_COUP_SUR = 12 # Seuil pour définir un Coup Sûr
TOTAL_SOURCES = 20           # Nombre total de sources simulées

# --- Fonction principale d'analyse ---
def analyze_raw_data(raw_data_filepath):
    """Charge les données brutes et calcule le consensus pour identifier les Coups Sûrs pour tous les types de pronostics."""
    
    try:
        df_raw = pd.read_csv(raw_data_filepath)
        print(f"\n--- 1. Données brutes chargées : {len(df_raw)} entrées ---")
    except FileNotFoundError:
        print(f"Erreur: Fichier introuvable à {raw_data_filepath}")
        return pd.DataFrame()
    
    # Liste des 5 types de pronostics à analyser
    prediction_types = [
        {'col_pred': 'raw_prediction_1X2', 'type': '1X2'},
        {'col_pred': 'raw_prediction_BTTS', 'type': 'BTTS (Les deux équipes marquent)'},
        {'col_pred': 'raw_prediction_OU25', 'type': 'Total Plus/Moins de 2.5'},
        {'col_pred': 'raw_prediction_YCards', 'type': 'Total Cartons Jaunes'}, 
        {'col_pred': 'raw_prediction_RBTT', 'type': 'Résultat + BTTS (Combiné)'}, # NOUVEAU COMBINÉ
    ]
    
    all_consensus_results = []
    
    print("\n--- 2. Calcul du nombre de votes par pronostic ---")

    # Génération d'une heure de match aléatoire par match_id pour simuler le temps réel
    # Si le match_id est 'm_123', il aura toujours la même heure simulée
    unique_match_ids = df_raw['match_id'].unique()
    
    # MODIFICATION 1 : Préparation des heures de match simulées
    match_times = {}
    for match_id in unique_match_ids:
        # Simule une heure de match entre 16:00 et 22:00
        hour = random.randint(16, 22)
        minute = random.choice(['00', '15', '30', '45'])
        match_times[match_id] = f"{hour:02d}:{minute}"


    for p_type in prediction_types:
        
        # Agrégation : Compter les votes pour ce type de pronostic
        consensus_df = df_raw.groupby(['match_id', 
                                         'home_team', 
                                         'away_team',
                                         p_type['col_pred']]).size().reset_index(name='vote_count')
        
        consensus_df['prediction_type'] = p_type['type']
        
        # Identification des Coups Sûrs pour ce type (le vote majoritaire atteint le seuil)
        df_coups_surs = consensus_df[consensus_df['vote_count'] >= MIN_SOURCES_FOR_COUP_SUR].copy()
        
        if not df_coups_surs.empty:
            df_coups_surs.rename(columns={p_type['col_pred']: 'raw_prediction'}, inplace=True)
            
            df_coups_surs['is_coup_sur'] = True
            df_coups_surs['total_sources'] = TOTAL_SOURCES
            
            # MODIFICATION 2 : Ajout de la colonne match_time au DataFrame final
            df_coups_surs['match_time'] = df_coups_surs['match_id'].map(match_times)
            
            all_consensus_results.append(df_coups_surs)
            
    if not all_consensus_results:
        print("Aucun Coup Sûr trouvé (aucun pronostic n'a atteint le seuil de 12 votes).")
        return pd.DataFrame()
        
    # Concaténer tous les résultats dans un seul DataFrame (vous devriez avoir 5 lignes si la simulation réussit)
    df_final = pd.concat(all_consensus_results, ignore_index=True)
    
    print(f"\n--- 4. Identification des Coups Sûrs Multi-Pronostics ({len(df_final)} trouvés) ---")
    print(df_final[['prediction_type', 'home_team', 'raw_prediction', 'vote_count', 'match_time', 'is_coup_sur']])
    
    # MODIFICATION 3 : Retourne la colonne match_time
    return df_final[['match_id', 
                     'home_team', 
                     'away_team', 
                     'raw_prediction',
                     'vote_count',
                     'total_sources',
                     'is_coup_sur',
                     'prediction_type',
                     'match_time' # <--- AJOUT CRITIQUE DANS LE RETOUR FINAL
                     ]]

# --- Exécution principale ---
if __name__ == "__main__":
    print(f"\n--- DÉBUT DE L'ANALYSE WINRUSH : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    all_files = os.listdir(backend_dir)
    raw_files = [f for f in all_files if f.startswith('raw_data_simulated_') and f.endswith('.csv')]
    
    if not raw_files:
        print("Erreur : Aucun fichier de données brutes trouvé. Exécutez collector.py d'abord.")
    else:
        latest_file = max(raw_files)
        latest_filepath = os.path.join(backend_dir, latest_file)
        
        df_results = analyze_raw_data(latest_filepath)
        
        if not df_results.empty:
            filename = f"consolidated_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df_results.to_csv(filename, index=False)
            print(f"\n--- Succès : Résultats consolidés stockés dans {filename} ---")