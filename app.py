from fastapi import FastAPI, HTTPException
from nudenet import NudeDetector
from pathlib import Path
from typing import List
import logging

app = FastAPI()

# Configurer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialiser le détecteur NudeNet
detector = NudeDetector()

@app.post("/classify")
async def classify_images(image_paths: List[str]):
    """
    Classifie un tableau d'images comme 'safe' ou 'unsafe' en fonction de leur contenu.
    Les chemins sont préfixés par '/data/images'.
    Args:
        image_paths (List[str]): Liste des chemins d'images à classer.
    Returns:
        dict: Dictionnaire avec les chemins d'images comme clés et leurs probabilités 'safe'/'unsafe' comme valeurs.
    """
    try:
        results = {}
        for image_path in image_paths:
            # Ajouter le préfixe /data/images
            full_path = f"/data/images{image_path}"
            image_file = Path(full_path)
            
            # Vérifier si le fichier existe
            if not image_file.is_file():
                logger.error(f"Image non trouvée : {full_path}")
                results[full_path] = {"error": "Image non trouvée"}
                continue
            
            # Détecter le contenu avec NudeDetector
            detections = detector.detect(str(image_file))
            logger.info(f"Détection pour {full_path}: {detections}")
            
            # Simuler les probabilités safe/unsafe
            unsafe_score = 0.0
            for detection in detections:
                if detection['class'] in ['FEMALE_GENITALIA_EXPOSED', 'BUTTOCKS_EXPOSED', 'FEMALE_BREAST_EXPOSED', 'MALE_BREAST_EXPOSED','ANUS_EXPOSED','MALE_GENITALIA_EXPOSED']:
                    unsafe_score = max(unsafe_score, detection['score'])
            
            results[image_path] = {
                "safe": 1.0 - unsafe_score,
                "unsafe": unsafe_score
            }
        
        return results
    
    except Exception as e:
        logger.error(f"Erreur lors de la classification : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")