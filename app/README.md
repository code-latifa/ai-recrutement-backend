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
## 🔐 Authentification

L’application utilise JWT pour sécuriser les endpoints.

- Login / Register
- Accès protégé par token
- Hash des mots de passe avec bcrypt
## 📧 Notifications

Lorsqu’un candidat est sélectionné pour une offre :
- Une notification est enregistrée en base
- Un email automatique est envoyé au candidat
