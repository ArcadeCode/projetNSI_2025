# Projet NSI 2025 [FR README]
Application mobile du projet finale NSI 2025 Sportify, une application de tracking de running pour coureurs. Ce projet ce décompose en plusieurs partie, ce repo contient l'application mobile du projet.

## Running, Building
Pour lancer le projet il faut d'abord obtenir le gestionnaire de dépendance [uv](), vous pouvez l'installer via pip :
```sh
pip install uv
```
Ensuite, simplement lancer le projet en utilisant le fichier `run.bat` :
```sh
./run.bat
```

## Décomposition de l'interface en objets Kivy
L'interface graphique est basé sur le framework kivy, voici présentement les différents objets utilisés :
- `App` = L'Objet principal auquel on va venir intégrer toute la structure.
- `Screen` = Un "écran" unique, chaque menu possède son propre écran.
- `Widget` = Une fenêtre, il pourra y avoir plusieurs fenêtres par écran.
- `Label` = Un simple texte.
- `Button` = Un simple bouton.
Ci-joint la liste des objets surcharger :
- `LabelVersion` = Une version de Label qui récupère la version du projet ( présente dans `.version` ) et l'affiche.

## Décomposition de la structure du projet
```
projet-nsi-2025
└───app
│   ├───fonts --------> Contain all fonts and font manager.
│   ├───labels -------> Contain labels and label tools
│   ├───tests --------> Contain tests for testing the app.
│   └───widgets ------> Contain widgets of the GUI
│
├───.python-version --> Contain python version.
├───.version ---------> Contain version project.
├───pyproject.toml ---> TOML project config file.
├───requirements.txt -> All packages needed to run the project.
│
├───Dockerfile -------> Docker file to generate a buildozer project and build the app for Android
├───run.bat ----------> Install dependencies and run the app on a computer
│
├───uv.lock ----------> Lock file for UV manager.
└───.gitignore -------> Ignore file for gitignore.
```