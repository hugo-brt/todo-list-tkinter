# 📝 To-Do List App (Tkinter, Python)

Une application de gestion de tâches simple, élégante et rapide, avec interface graphique responsive et dark mode, réalisée en Python avec Tkinter.

![Screenshot](screenshot.png)

---

## ✨ Fonctionnalités

- **Ajout, modification, suppression de tâches**
- **Gestion de la priorité** (tri automatique, champ numérique)
- **Marquer/démarquer une tâche comme faite**
- **Responsive :** l’interface s’adapte à la taille de la fenêtre
- **Dark mode / Light mode** à la demande
- **Enregistrement automatique** des tâches dans un fichier `tasks.json` local

---

## 🚀 Installation

### **1. Depuis Python (toutes plateformes)**

- **Pré-requis :** Python 3.x (préinstallé sur Linux/Mac, téléchargeable sur [python.org](https://www.python.org/))
- Clone ce dépôt ou télécharge le fichier `todo_gui.py`

```sh
git clone https://github.com/hugo-brt/todo-list-tkinter.git
cd todo-list-tkinter
python todo_gui.py

2. Version Windows (.exe, sans Python)

    Télécharge la dernière version depuis le dossier dist/ ou le fichier .exe fourni.

    Double-clique sur todo_app.exe (aucune installation nécessaire !)

    Si vous ne voyez rien s’ouvrir, vérifiez que tasks.json est accessible en écriture dans le dossier.

3. Créer votre propre exécutable

Si vous souhaitez le générer vous-même :
pip install pyinstaller
pyinstaller --onefile --noconsole todo_app.py


🖥️ Utilisation

    Ajouter une tâche : Renseignez le texte et éventuellement une priorité, cliquez sur “Add Task”.

    Modifier la priorité : Sélectionnez une tâche, changez la valeur puis cliquez sur “Modify Priority”.

    Dark/Light mode : Changez de thème en un clic.

    Supprimer ou marquer : Sélectionnez la tâche et utilisez les boutons du bas.

📦 Fichiers importants

    todo_gui.py : le programme principal

    tasks.json : la sauvegarde locale des tâches (créée automatiquement)

    screenshot.png : une capture d’écran

❓ FAQ

Q : Est-ce que mes tâches sont sauvegardées automatiquement ?
R : Oui, tout est stocké dans le fichier tasks.json local.

Q : L’exécutable ne démarre pas !
R : Vérifiez que vous avez bien extrait le fichier de l’archive, et que tasks.json n’est pas bloqué par un antivirus ou en lecture seule.

Q : Puis-je ajouter un fond ou des fonctionnalités ?
R : Bien sûr ! Forkez le projet, proposez une Pull Request ou modifiez-le pour vos besoins.
🤝 À propos

Ce projet a été réalisé pour le portfolio GitHub, pour apprendre et démontrer :

    Tkinter (GUI Python)

    Gestion de fichiers et de données JSON

    Responsive Design en Tkinter

    Packaging en exécutable (.exe)

Auteur : Hugo Birobent
