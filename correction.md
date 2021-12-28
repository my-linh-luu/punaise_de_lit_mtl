# Points développés dans le travail

+ A1 : La base de données vide `data.db` existe déjà préalablement dans le répertoire `db`. Celle-ci
contient toutes les tables vides qui sont décrites dans `data.sql`. Afin de tester
cette fonctionnalité, avant même de lancer le site, à partir de la racine du projet,
lancer la commande 

```
python fetch_data.py
```

Ce script s'occupe de récupérer toutes les déclarations à ce jour sur le site de
la ville et les ajoutent à la base de données `data.db`, dans la table `declarations_ville`. Afin de vérifier que la
base de données soit bel et bien remplie, vous pouvez inscrire cette commande
à partir de la racine du projet :
```
sqlite3 db/data.db
```
Puis, une fois dans `sqlite3`, lancer cette commande :
```
select * from declarations_villes;
```
Ceci devrait afficher toutes les déclarations de la ville qui ont été ajoutées dans
la base de données.

+ A2 : Une fois la base de données remplie, lancer l'application `flask` à partir de
la racine du projet en tapant simplement `make`. Ensuite, en cliquant sur le lien généré,
cela devrait vous mener directement sur la page d'accueil du site. Pour tester cette fonctionnalité,
simplement inscrire dans la barre de recherche principale un nom de quartier ou un arrondissement.
Pour le nom de quartier, vous pouvez essayez avec `Anjou` ou `Beaurivage`. Pour le nom d'arrondissement, vous pouvez
tester `verdun`. Il est à noter que la recherche se fait sans tenir compte des cases, donc `anjou` est équivalent à `Anjou`. Par contre, les accents sont différents donc
 `montreal` n'affichera rien tandis que `montréal` affichera les déclarations. Vous pouvez également tester le programme
avec un nom incomplet par exemple `est`, la barre de recherche va chercher tous les noms de quartiers ou d'arrondissement
qui contiennent ce terme. Une des résultats trouvés, elle va automatiquement vous rediriger vers une autre page contenant
un tableau avec toutes les déclarations trouvées. Lorsque vous ne rentrez rien dans la bare de recherche et que vous cliquez sur
`Rechercher`, un message d'erreur devrait s'afficher. Lorsqu'aucun résultats n'a été trouvés, un message d'erreur devrait
également s'afficher. 

+ A3 : Pour le BackgroundScheduler, la fonction `fetch_data_periodicaly` s'occupe de mettre à jour la base de données à minuit à chaque jour.
Elle s'occupe de vérifier ligne par ligne si la déclaration est déjà dans la base de données. Si c'est le cas, elle ne l'ajoutera pas. Si le numéro
de déclaration a été supprimé par un utilisateur, elle ne l'ajoutera pas non plus lors de la mise à jour. Afin de tester cette fonctionnalité, vous
pouvez changer les paramètres du décorateur `@scheduler.scheduled_job('cron', hour=0)`, remplacez `hour=0` par une heure qui vous convient et vous pouvez également
ajouter `minute=` afin de précisez à la minute près à quel moment vous voulez que la mise à jour soit effectuée. Puis, vous devriez voir apparaître sur 
la console un message `fetching...` qui indique que l'application est en train de mettre à jour sa base de données. Cela devrait durer plusieurs minutes (4-5).
Attendre jusqu'à ce que la console affiche `Base de données à jour` qui indique la fin de la mise à jour. Ensuite, vous pouvez simplement vérifier dans
la base de données si les données ont bel et bien été mise à jour.

+ A4 : Ce service REST se trouve à la route `/api/declarations`. Afin de le tester, simplement ouvrir une application qui teste les services REST comme `YARC` ou `POSTMAN`. Puis, inscrire dans la barre de recherche
le lien vers le site suivi de `/api/declarations` et ajouter les paramètres  `du` et `au`, exemple `http://127.0.0.1:5000/api/declarations?du=2012-01-01&au=2012-03-01`. Ceci devrait afficher la liste des déclarations. Il est à noter
que vous pouvez également simplement inscrire le lien directement dans le fureteur.
Pour le `RAML`, aller dans `/doc`. Le premier élément présenté est `/api/declarations`. Cliquez sur le bouton `GET`. Les informations pour ce service seront affichées.

+ A5 : Le formulaire de recherche selon les dates est juste en-dessous de la barre de recherche principale, sur la page d'accueil. Pour tester cette fonctionnalité,
inscrire deux dates en format ISO 8601 ex : `2012-01-01` et `2013-01-01` dans le champs `Du` et `Au`. Laissez le champs `Quartier` sur `Tous les quartiers`. Ceci devrait charger un tableau sur
la même page qui contient toutes les déclarations définies entre ces dates. L'affichage pourrait prendre quelques secondes, mais une animation
indique lorsque la recherche est en train de rouler. Lorsque l'utilisateur n'entre pas deux dates et appuie sur `Rechercher`, un message d'erreur s'affiche. Lorsque
les formats des dates ne sont pas corrects, un message d'erreur s'affiche également. Il est a noter que cette fonctionnalité envoie une requête ajax à la route `/api/declarations` définie plus tôt.

+ A6 : Afin de filtrer la recherche en `A5` par quartier, après avoir inscrit les dates, dans le champs `Quartier`, sélectionnez dans la liste déroulante un quartier. Maintenant, en cliquant sur `Rechercher`, ceci devrait uniquement afficher
un tableau contenant les déclarations entre ces dates pour le quartier spécifié. Il est à noter que cette fonctionnalité envoie une requête AJAX à la route `/api/declarations` définie plus tôt.

+ C1 : Ce service REST est défini sous la route `/api/declarations/quartiers`. Son `RAML` est défini sous `/doc`. Simplement cliquer sur `GET` pour obtenir les informations
sur ce service.

+ D1 : Ce service REST est défini sous la route `/api/declaration` avec la methode `POST`. Regarder son RAML pour savoir comment bien définir la requête json à remplir. Une fois la déclaration envoyée,
celle-ci est ajoutée à la table `declarations_internes`, afin de distinguer les déclarations de la villes qui sont dans la table `declarations_villes` et celles provenant de notre site.
De plus, son `json_schema` se nomme `declaration_insert_schema` et est défini dans le fichier `schemas.py` situé à la racine du projet. Pour tester le schema, vous pouvez ommettre un champs lors de 
l'envoie de la déclaration, un message d'erreur devrait s'afficher.
Pour effectuer une déclaration sur le site, dans le menu, cliquer sur `Faire une déclaration`. Une page contenant un formulaire à remplir devrait s'afficher. Si le formulaire n'est pas bien rempli
(champs pas tous remplis, date invalide), un message d'erreur apparait. À noter que lors d'un `GET` de cette page, c'est la route `/declaration` qui est appelée. Une fois que le formulaire est envoyé,
la requête AJAX est envoyée au service REST défini plus haut.

+ D2 : Le service REST est défini sous la route `/api/declaration/{id}` avec la méthode `DELETE`. Voir son RAML sous `/doc`. **Important de noter que ce service permet uniquement de supprimer les déclarations dans le tableau des déclarations à l'interne, donc les déclarations qui ont été
ajoutés sur ce site**. Elle ne supprime pas les déclarations de la ville dans la table `declarations_ville`. Afin de vérifier cette fonctionnalité,
il faut s'assurer d'avoir préalablement ajoutées des déclarations dans le formulaire de déclaration ou par le service REST en `D1`. Noter les identifiants associés
avec chaque déclaration ajoutée, puis inscrire le numéro de l'id pour ce service.

+ D3 : Toujours sur la page d'accueil, le bouton `Supprimer` permet de supprimer les déclarations qui sont retrounées par la recherche par date et quartier. L'utilisateur doit absolument sélectionner un nom de quartier avant de supprimer, sinon
un message d'erreur indique que l'utilisateur ne peut pas supprimer tous les quartiers entre ces dates. Cette application invoque avec des appels AJAX la route `/api/declarations` avec la méthode `DELETE`, voir son RAML sous `/doc`. Si la suppression fonctionne,
un message de succès s'affiche. Si les déclarations n'existent pas et qu'on tente de supprimer, un message d'erreur s'affiche. Les numéros de déclaration des déclarations supprimées sont ensuite ajoutées dans la table
`declarations_supprimees` afin de ne pas les ajouter lors de la synchronisation quotidienne. À noter que les suppressions affectent les déclarations de la ville seulement (dans la table `declarations_ville`), et non 
celles ajoutées par l'utilisateur sur le site. Afin de vérifier que les suppressions sont préservées, vous pouvez effectuer les changements au BackgroundScheduler défini en `A3` afin de le lancer plus tôt. Une fois la mise à jour terminée, 
vérifier dans la base de données si les déclarations qui se trouvent dans la table `declarations_supprimees` ont été ajoutées à la base de données.

+ E1 : Ce service est défini sous la route `/api/user`. Son RAML se situe sous `/doc` afin d'avoir les spécifications sur le service. Son `json_schema` se nomme `user_insert_schema` et est défini dans `schemas.py`.

+ E2 : Pour pouvoir se créer un compte utilisateur, cliquer sur `Se connecter` dans le menu et cliquer sur le lien `Créez un profil`. Le formulaire pour créer un compte s'affiche. Cette fonctionnalité invoque ensuite par appels AJAX
le service défini en `E1`. Une fois le compte créé, l'utilisateur est redirigé vers la page pour se connecter. Il peut ensuite entrer ses informations. Si les informations entrées par l'utilisateur ne sont pas valides,
un message à cet effet est affiché. Une fois l'utilisateur connecté, le menu présente désormais trois nouvels onglets. L'onglet `Modifier les quartiers à surveiller` permet à l'utilisateur d'accéder à une page pour changer 
les quartiers qui sont surveillés par lui. L'onglet `Ajouter une photo de profil` permet à l'utilisateur de téléverser une photo sous les formats `jpeg` ou `png` seulement. Le blob de la photo est conservée dans la table `pictures` et
l'identifiant généré automatiquement est associé à l'utilisateur. Une fois une photo associée à cet utilisateur, la photo s'affiche sur la page. Si l'utilisateur se déconnecte et se reconnecte, la photo de profil précédemment téléversée
devrait encore s'afficher. Finalement, l'onglet `Se déconnecter` permet à l'utilisateur de se déconnecter et il est redirigé sur la page d'accueil. Si l'utilisateur n'est pas connecté et qu'il tente d'accéder à la page `/modification` 
pour changer les quartiers surveillés ou `/upload_photo` pour ajouter une photo de profil, une boîte lui demandant de s'authentifier s'affiche. Le cas échéant, un message d'erreur s'affiche.