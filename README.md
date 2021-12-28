# Recherche de données sur les exterminations de punaises de lit à Montréal 

Ce site permet d'avoir accès en temps réel aux données disponibles sur les exterminations de punaises de lit à Montréal. Il met à la disposition de l'utilisateur une bare de recherche qui lui permet de rechercher les informations déclarations émises selon des quartiers précis. Le site permet également à un utilisateur de s'inscrire dans

# Suivre ces étapes au lancement du programme

#### 1. Préalables au bon fonctionnement du site

S'assurer d'avoir téléchargé `raml2html` afin de visualiser la documentation :

```
npm i -g raml2html
```

Avec `pip install` :
+ flask
+ pandas
+ apscheduler
+ flask-json-schema

#### 2. Remplir la base de données
Une base de donnée vide au nom de `data.db` est déjà fournis avec le programme, situé dans le dossier `db`.
Afin de remplir les tables des données de la ville, avant même de lancer le programme flask, à partir de
la racine de projet, lancer la commande :
```
python fetch_data.py
```
Le fichier `fetch_data.py` contient le script python pour récupérer les données.

#### 3. Lancer le programme

Pour lancer le programme, simplement taper la commande `make`, ceci générera aussi le
`doc.html` à partir du `doc.raml`. Vous pouvez maintenant utiliser le site.
