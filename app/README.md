# AI Recruitment Backend

Backend pour une plateforme de recrutement utilisant l'IA générative pour analyser les CV, les offres d'emploi et effectuer du matching candidat-offre.

---

## 🚀 Fonctionnalités

- Gestion des utilisateurs : candidats et recruteurs
- Gestion des CV et des offres d'emploi
- Analyse automatisée des CV et des offres via IA
- Moteur de matching basé sur embeddings vectoriels
- API RESTful avec FastAPI
- Connexion à une base de données PostgreSQL
- Journalisation et scoring des résultats

---

## 🛠️ Tech Stack

- **Framework Web** : FastAPI
- **Base de données** : PostgreSQL + SQLAlchemy
- **IA générative** : LangChain, OpenAI, MCP
- **Vector Store** : ChromaDB
- **Utilitaires** : python-dotenv, loguru, requests

---

## 📦 Installation

1. **Cloner le projet**

```bash
git clone https://github.com/latifa-code/ai-recruitment-backend.git
cd ai-recruitment-backend
  Test & tâches – Hanane (Backend / Auth & DB setup)

#(hanane achoukri)#Ce document explique comment installer, configurer et tester le backend du projet AI Recruitment.

🔧 Prérequis

Avant de commencer, assure-toi d’avoir installé :

Python 3.10+

Docker Desktop 4.57.0 (ou version proche)

Git

pip (gestionnaire de paquets Python)

🐳 1. Installation et configuration de Docker & PostgreSQL
1️⃣ Installer Docker

Télécharger Docker Desktop depuis :
https://www.docker.com/products/docker-desktop/

Lancer Docker Desktop

Vérifier qu’il est bien démarré :

docker --version

2️⃣ Lancer PostgreSQL dans un container Docker

Exécuter la commande suivante :

docker run --name pg-ai \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ai_recrutement \
  -p 5432:5432 \
  -d postgres:15


👉 Vérifier que le container tourne :

docker ps

3️⃣ Créer les tables de la base de données

Se placer à la racine du projet (là où se trouve le dossier app) puis exécuter :

type app\core\schema.sql | docker exec -i pg-ai psql -U postgres -d ai_recrutement


✅ Si tu vois CREATE TABLE, CREATE INDEX, CREATE TRIGGER, alors la base est prête.

🐍 2. Installation du backend FastAPI
1️⃣ Créer et activer un environnement virtuel
python -m venv venv
venv\Scripts\activate

2️⃣ Installer les dépendances
pip install -r requirements.txt


⚠️ Important (bcrypt compatible avec passlib) :

pip install bcrypt==4.0.1

⚙️ 3. Configuration .env

Créer un fichier .env à la racine du backend avec le contenu suivant :

DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ai_recrutement
JWT_SECRET=dev_secret_123
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:8501,http://localhost:3000
APP_NAME=AI Recruitment API
ENV=dev

🚀 4. Lancer l’API
uvicorn app.main:app --reload


Si tout est correct, tu verras :

Uvicorn running on http://127.0.0.1:8000

📖 5. Tester l’API (Swagger)

Ouvrir dans le navigateur :

👉 Swagger UI

http://localhost:8000/docs

Tests recommandés (ordre important) :

1️⃣ Health check

GET /health


→ doit retourner { "status": "ok" }

2️⃣ Créer un utilisateur

POST /api/auth/register


Body exemple :

{
  "email": "test@example.com",
  "password": "123456",
  "role": "candidat"
}


3️⃣ Se connecter

POST /api/auth/login


4️⃣ Tester l’utilisateur connecté

GET /api/auth/me


➡️ Ajouter le token JWT dans Authorize (Swagger).

✅ Résumé de mon travail (Hanane)

Installation et configuration de Docker

Mise en place de PostgreSQL via container

Création des tables SQL (schema.sql)

Configuration de l’environnement backend

Lancement de FastAPI

Tests des routes authentification via Swagger