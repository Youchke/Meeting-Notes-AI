# 🎙️ Meeting Notes AI

**Transformez vos réunions en résumés structurés grâce à l'IA.**

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Meeting Notes AI** est une application web moderne qui automatise la prise de notes. Elle transcrit vos fichiers audio/vidéo et génère des résumés intelligents (décisions, actions, points clés) en utilisant la puissance des modèles **Google Gemini**.

---

## ✨ Fonctionnalités Clés

*   🚀 **Interface Web Moderne** : Une expérience utilisateur fluide avec glisser-déposer.
*   🧠 **Intelligence Artificielle** : Propulsé par Google Gemini 1.5/2.0 Flash pour une précision inégalée.
*   📝 **Transcription & Résumé** : Obtenez le verbatim complet ET une synthèse structurée.
*   🔒 **Confidentialité Totale** : Aucun stockage permanent. Vos fichiers sont traités en mémoire et supprimés immédiatement.
*   📋 **Copie Rapide** : Copiez le texte généré en un clic pour l'utiliser ailleurs.
*   🐳 **Déploiement Facile** : Entièrement conteneurisé avec Docker pour une installation en une commande.

---

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir :

*   [Docker](https://www.docker.com/products/docker-desktop) et Docker Compose installés.
*   Une clé API **Google Gemini** (disponible gratuitement sur [Google AI Studio](https://aistudio.google.com/app/apikey)).

---

## 🚀 Installation et Démarrage

### 1. Cloner le projet
```bash
https://github.com/Youchke/Meeting-Notes-AI.git

```

### 2. Configurer la clé API
Créez un fichier `.env` à la racine du projet et ajoutez votre clé :

```env
GEMINI_API_KEY=votre_clé_api_ici
```

### 3. Lancer l'application
Utilisez Docker Compose pour construire et démarrer le serveur :

```bash
docker-compose up --build
```

### 4. Accéder à l'interface
Ouvrez votre navigateur et allez sur :
👉 **http://localhost:8000**

---

## 📂 Structure du Projet

```
Meeting-Notes-AI/
├── Dockerfile              # Configuration de l'image Docker
├── docker-compose.yml      # Orchestration des services
├── requirements.txt        # Dépendances Python
├── .env                    # Variables d'environnement (API Key)
├── src/
│   ├── app.py              # Backend FastAPI
│   ├── pipelines.py        # Logique de traitement IA
│   ├── static/             # Frontend (HTML, CSS, JS)
│   ├── gemini_api_interaction/ # Client API Gemini
│   ├── speech_transcriber/     # Module de transcription
│   ├── meeting_summarizer/     # Module de résumé
│   └── generate_meeting_summary/ # Génération de la structure
```

---

## 🛡️ Gestion des Erreurs

*   **Erreur 429 (Resource Exhausted)** : L'application gère automatiquement les limites de l'API Gemini en attendant quelques secondes avant de réessayer.
*   **Fichiers trop volumineux** : Gemini gère nativement les fichiers audio volumineux, mais assurez-vous d'avoir une connexion stable.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une "Issue" ou une "Pull Request" pour suggérer des améliorations.

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
