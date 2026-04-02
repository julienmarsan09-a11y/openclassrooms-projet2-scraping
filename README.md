# OpenClassrooms - Projet 2 : Web Scraping

## À propos

Script Python de scraping développé pour le Projet 2 de ma formation en tant que développeur d'application Python chez OpenClassrooms. L'objectif est de mettre en place un système automatisé de collecte des prix sur le site [Books to Scrape](http://books.toscrape.com/).

## Contexte

Suivre manuellement les prix des livres sur les librairies en ligne est une tâche chronophage. Ce programme permet d'automatiser cette collecte en récupérant les informations produits (prix, disponibilité, description...) et en les exportant directement en fichier CSV.

## Fonctionnalités

Le projet se décompose en 4 phases :

1. **Phase 1** — Extraction des données d'un seul livre (titre, prix, UPC, description, catégorie, note, image, etc.) vers un fichier CSV.
2. **Phase 2** — Extraction de tous les livres d'une catégorie.
3. **Phase 3** — Extraction de l'ensemble des livres du site de toutes les catégories.
4. **Phase 4** — Téléchargement des images de couverture de chaque livre avec l'UPC comme nom de fichier.

## Installation

1. Clonez le dépôt :
```
git clone https://github.com/julienmarsan09-a11y/openclassrooms-projet2-scraping.git
cd openclassrooms-projet2-scraping
```

2. Créez et activez un environnement virtuel :
```
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux / macOS
```

3. Installez les dépendances :
```
pip install -r requirements.txt
```

## Utilisation
```
Pour lancer le script 
```
Exécutez la commande suivante :
`python main.py`


## Résultat du script
```
Les données sont exportées en CSV dans le dossier **donnees_extraites / csv** du projet et les images sont exportées dans le dossier **donnees_extraites / images**

```