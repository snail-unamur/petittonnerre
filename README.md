# 🚀 Installation de FastAPI (macOS / Homebrew Python)

Ce guide explique comment installer **FastAPI** proprement sur macOS sans casser l’environnement système Python.

---

## 🧩 1. Créer un environnement virtuel

Dans ton terminal, place-toi dans ton projet, puis exécute :

```bash
python3 -m venv .venv
```
ou
```bash
python -m venv .venv
```

Cela crée un dossier `.venv` contenant ton environnement isolé.

---

## ⚙️ 2. Activer l’environnement

Active-le avec :

```bash
source .venv/bin/activate
```

Tu devrais voir `(.venv)` au début de ta ligne de commande — cela indique que ton environnement virtuel est actif.

---

## 📦 3. Installer FastAPI et Uvicorn

Une fois l’environnement activé, installe FastAPI et le serveur Uvicorn :

```bash
pip install fastapi uvicorn
```

---

## 🚀 4. Lancer le serveur FastAPI

Toujours dans ton environnement virtuel :

```bash
uvicorn main:app --reload
```

Puis ouvre ton navigateur à [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Tu verras ta première réponse FastAPI 🎉

---

## 🧹 5. (Optionnel) Désactiver l’environnement virtuel

Quand tu as fini de travailler :

```bash
deactivate
```

---

## 💡 Astuce

Pour éviter d’oublier d’activer ton environnement, tu peux créer un alias dans ton shell (zsh ou bash) :

```bash
alias actvenv='source .venv/bin/activate'
```

Ensuite, il te suffira de taper :
```bash
actvenv
```

---

✅ **Tu es prêt à développer avec FastAPI sur macOS !**
