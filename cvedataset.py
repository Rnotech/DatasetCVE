import os
import json

# Chemin vers le répertoire principal des CVE (exemple : './cvelistV5/cves/')
CVE_BASE_PATH = './cvelistV5/cves/'

# Liste des années pour les CVE que nous voulons traiter
YEARS = [str(year) for year in range(1999, 2025)]

# Fonction pour générer des questions-réponses à partir des données CVE
def generate_qa(cve_data):
    questions_answers = []
    
    cve_id = cve_data.get('cveMetadata', {}).get('cveId', 'Non spécifié')
    descriptions = cve_data.get('containers', {}).get('cna', {}).get('descriptions', []).get('value', 'Non spécifié')
    references = cve_data.get('containers', {}).get('cna', {}).get('references', []).get('url','Non spécifié')
    # Génération des questions-réponses
    questions_answers.append({
        "question": f"Expliquer le {cve_id} ?",
        "answer": descriptions
    })
    questions_answers.append({
        "question": f"Quelle est l'ID du CVE associé à cette vulnérabilité : '{descriptions}' ?",
        "answer": cve_id
    })
    questions_answers.append({
        "question": f"Où puis-je trouver plus d'informations sur la vulnérabilité du {cve_id} ?",
        "answer": references
    })

    return {
        "cve_id": cve_id,
        "chat": questions_answers
    }

# Fonction principale pour lire les fichiers CVE et générer le dataset
def process_cve_files():
    dataset = []
    
    # Parcours des répertoires par année
    for year in YEARS:
        year_path = os.path.join(CVE_BASE_PATH, year)
        
        # Vérification que le répertoire existe
        if not os.path.isdir(year_path):
            continue

        # Parcours des fichiers JSON dans le répertoire de l'année
        for root, dirs, files in os.walk(year_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    
                    # Lecture du fichier JSON
                    with open(file_path, 'r') as f:
                        try:
                            cve_data = json.load(f)
                            qa_entry = generate_qa(cve_data)
                            dataset.append(qa_entry)
                        except json.JSONDecodeError:
                            print(f"Erreur de lecture du fichier JSON : {file_path}")
    
    # Sauvegarde des données générées dans un fichier de sortie JSON
    with open('fine_tuning_dataset.json', 'w', encoding='utf-8') as outfile:
        json.dump(dataset, outfile, ensure_ascii=False, indent=2)

    print("Dataset généré avec succès !")

# Exécution du script
if __name__ == "__main__":
    process_cve_files()
