🚀 AI Recruitment – Backend (FastAPI)

Backend du projet AI Recruitment, une plateforme intelligente de recrutement basée sur l’IA.
Ce backend fournit une API REST sécurisée pour la gestion des utilisateurs, CV, offres d’emploi et matching.

🧱 Stack Technique

Python 3.10+

FastAPI

PostgreSQL

Docker

SQLAlchemy

JWT (Authentification)

Passlib + bcrypt

ChromaDB (prévu pour le vector store / IA)

📁 Structure du projet
ai-recrutement-backend/
│
├── app/
│   ├── main.py                # Point d’entrée FastAPI
│   ├── api/                   # Routes (auth, candidats, offres, etc.)
│   ├── core/                  # Config, DB, sécurité, schéma SQL
│   ├── models/                # Modèles SQLAlchemy
│   ├── schemas/               # Schémas Pydantic
│   ├── services/              # Logique métier
│   ├── ai/                    # Modules IA (analyse CV, matching)
│   ├── vector_store/          # ChromaDB
│   └── utils/                 # Outils (logging, scoring)
│
├── requirements.txt
├── .gitignore
└── README.md

✅ Prérequis

Avant de commencer, assure-toi d’avoir installé :

Python 3.10 ou plus

Docker Desktop (v4.57.0 ou proche)

Git

Vérification :

python --version
docker --version
git --version

🐳 1. Lancer PostgreSQL avec Docker
1️⃣ Démarrer Docker Desktop

Assure-toi que Docker est bien lancé (icône verte).

2️⃣ Créer le container PostgreSQL
docker run --name pg-ai \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ai_recrutement \
  -p 5432:5432 \
  -d postgres:15


Vérification :

docker ps

🗄️ 2. Initialiser la base de données

Créer les tables à partir du schéma SQL.

Depuis la racine du projet :

type app\core\schema.sql | docker exec -i pg-ai psql -U postgres -d ai_recrutement


Vérifier les tables :

docker exec -it pg-ai psql -U postgres -d ai_recrutement -c "\dt"

🐍 3. Installer le backend FastAPI
1️⃣ Créer et activer un environnement virtuel
python -m venv venv
venv\Scripts\activate

2️⃣ Installer les dépendances
pip install -r requirements.txt


⚠️ Important (compatibilité auth) :

pip install bcrypt==4.0.1

⚙️ 4. Configuration .env

Créer un fichier .env à la racine du projet :

DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ai_recrutement
JWT_SECRET=dev_secret_123
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:8501,http://localhost:3000
APP_NAME=AI Recruitment API
ENV=dev


⚠️ Le fichier .env est ignoré par Git.

🚀 5. Lancer l’API
uvicorn app.main:app --reload


Si tout est correct :

Uvicorn running on http://127.0.0.1:8000

🧪 6. Tester l’API (Swagger)
Swagger UI

👉 http://127.0.0.1:8000/docs

Health check
GET /health


Réponse attendue :

{ "status": "ok" }

Authentification – ordre recommandé
1️⃣ Register
POST /api/auth/register


Body :

{
  "email": "test@example.com",
  "password": "123456",
  "role": "candidat"
}

2️⃣ Login
POST /api/auth/login


Copier le access_token.

3️⃣ Tester une route protégée

Cliquer sur Authorize dans Swagger :

Bearer <ACCESS_TOKEN>


Puis :

GET /api/auth/me

🔐 Sécurité

Hash des mots de passe avec bcrypt

Authentification JWT

Rôles : candidat, recruteur, admin

Dépendances FastAPI pour la protection des routes