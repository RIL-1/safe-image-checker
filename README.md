# Safe Image Checker

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9-blue?logo=python" alt="Python 3.9">
  <img src="https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi" alt="FastAPI 0.115.0">
  <img src="https://img.shields.io/badge/NudeNet-3.0.2-purple" alt="NudeNet 3.0.2">
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?logo=docker" alt="Docker ready">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

Microservice HTTP qui analyse des images et les classe comme **safe** ou **unsafe** à l'aide de [NudeNet](https://github.com/notAI-tech/NudeNet).

## Fonctionnement

Le service expose une API REST (FastAPI). Pour chaque image demandée, NudeNet détecte des zones sensibles (nudité, parties du corps exposées, etc.) et calcule un score de confiance. Le résultat est une probabilité **safe** / **unsafe** basée sur le score le plus élevé parmi les classes considérées comme sensibles.

Les images doivent être accessibles localement dans le conteneur sous le répertoire `/data/images`.

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) (recommandé)
- ou Python 3.9+ avec les dépendances système pour OpenCV

## Démarrage rapide (Docker)

```bash
docker build -t safe-image-checker .

docker run -d \
  --name safe-image-checker \
  -p 5000:5000 \
  -v /chemin/vers/vos/images:/data/images:ro \
  safe-image-checker
```

Remplacez `/chemin/vers/vos/images` par le dossier local contenant les images à analyser. Le montage est en lecture seule (`:ro`).

## API

### `POST /classify`

Analyse une ou plusieurs images et retourne un score **safe** / **unsafe** pour chacune.

**Corps de la requête** — tableau JSON de chemins relatifs (sans le préfixe `/data/images`) :

```json
["photo1.jpg", "dossier/photo2.png"]
```

**Réponse** — objet JSON indexé par le chemin demandé :

```json
{
  "photo1.jpg": {
    "safe": 0.92,
    "unsafe": 0.08
  },
  "dossier/photo2.png": {
    "safe": 0.15,
    "unsafe": 0.85
  }
}
```

En cas d'image introuvable, la clé correspondante contient une erreur :

```json
{
  "inexistante.jpg": {
    "error": "Image non trouvée"
  }
}
```

**Exemple avec curl :**

```bash
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '["mon-image.jpg"]'
```

### Documentation interactive

Une fois le service lancé, la documentation Swagger est disponible sur [http://localhost:5000/docs](http://localhost:5000/docs).

## Installation locale (sans Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install nudenet==3.0.2
```

Sur Linux, installez aussi les bibliothèques système nécessaires à OpenCV :

```bash
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
```

Lancez le serveur en pointant vers un dossier d'images :

```bash
mkdir -p /data/images
# copiez vos images dans /data/images
uvicorn app:app --host 0.0.0.0 --port 5000
```

## Classes détectées comme sensibles

Le score **unsafe** correspond au maximum des scores de confiance parmi les classes suivantes :

| Classe |
|--------|
| `FEMALE_GENITALIA_EXPOSED` |
| `MALE_GENITALIA_EXPOSED` |
| `FEMALE_BREAST_EXPOSED` |
| `MALE_BREAST_EXPOSED` |
| `BUTTOCKS_EXPOSED` |
| `ANUS_EXPOSED` |
| `FEET_COVERED` |

Le score **safe** vaut `1.0 - unsafe`.

## Stack technique

| Composant | Version |
|-----------|---------|
| Python | 3.9 |
| FastAPI | 0.115.0 |
| Uvicorn | 0.32.0 |
| NudeNet | 3.0.2 |

## Sécurité & architecture

Ce service est conçu pour être utilisé **uniquement en interne** dans une infrastructure Docker et n'embarque **aucun mécanisme d'authentification**.

Dans mon architecture, il est exposé via un réseau Docker interne, avec l'authentification, le rate-limiting et le TLS gérés en amont par un reverse proxy.

## Limitations

- Les scores sont des estimations basées sur un modèle de détection d'objets ; ils ne constituent pas une garantie absolue.
- Seules les images présentes dans `/data/images` (ou un volume monté à cet emplacement) peuvent être analysées.
- Le service ne télécharge pas d'images depuis Internet : il lit uniquement des fichiers locaux.

## Licence

Projet personnel.
