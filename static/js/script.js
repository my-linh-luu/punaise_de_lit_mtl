/*
Permet de valier des dates entrees, si les dates sont valides, va envoyer une
requete au serveur pour charger les declarations entre ses dates
 */
function chercherParDates() {
    let dateDebut = document.getElementById("date_debut").value;
    let dateFin = document.getElementById("date_fin").value;
    let errorContainer = document.getElementById("error_date");
    let msgContainer = document.getElementById("message");
    if (dateDebut == null || dateDebut === "" || dateFin == null
        || dateFin === "") {
        errorContainer.innerHTML = "Les deux dates doivent contenir une valeur.";
    } else if (!dateDebut.match(/(\d{4})-(\d{2})-(\d{2})/)
        || !dateFin.match(/(\d{4})-(\d{2})-(\d{2})/)) {
        errorContainer.innerHTML = "Les dates n'ont pas le bon format " +
            "(YYYY-MM-DD).";
    } else { // ok, valide
        errorContainer.innerHTML = "";
        chargerDeclarationEntreDates(dateDebut, dateFin);
        // permet de vider le container des alertes
        msgContainer.className = "";
        msgContainer.innerHTML = "";
    }
}

/*
Valide les dates entree, si valides, va envoyer une requete au serveur pour
supprimer les declarations entre les dates specifiees et selon le quartier
 */
function supprimerDeclarationParQuartier() {
    let dateDebut = document.getElementById("date_debut").value;
    let dateFin = document.getElementById("date_fin").value;
    let errorContainer = document.getElementById("error_date");
    let quartier = document.getElementById("quartier");
    if (dateDebut == null || dateDebut === "" || dateFin == null
            || dateFin === "") {
        errorContainer.innerHTML = "Les deux dates doivent contenir une " +
            "valeur.";
    } else if (!dateDebut.match(/(\d{4})-(\d{2})-(\d{2})/) ||
        !dateFin.match(/(\d{4})-(\d{2})-(\d{2})/)) {
        errorContainer.innerHTML = "Les dates n'ont pas le bon format " +
            "(YYYY-MM-DD).";
    } else if (quartier.options[quartier.selectedIndex].value === "tous"){
        errorContainer.innerHTML = "Vous devez sélectionner un quartier " +
            "avant de pouvoir supprimer.";
    } else {
        errorContainer.innerHTML = "";
        confirmerSuppression(dateDebut, dateFin,
            quartier.options[quartier.selectedIndex].value);
    }
}

/*
Affiche le tableau contenant les declarations entre les dates et selon le
quartier
 */
function chargerDeclarationEntreDates(dateDebut, dateFin) {
    getDeclarationsByDates(dateDebut, dateFin, "rechercher_qr")
        .then(quartiers =>
            creerTable(quartiers));
}

/*
Envoie une requete ajax afin de supprimer les declarations entre les dates et
selon le quartier. Si la suppression est realisee, affiche un message pour
l'indiquer. Sinon, affiche un message d'erreur
 */
function confirmerSuppression(dateDebut, dateFin, quartier) {
    let message = document.getElementById("message");
    let tableContainer = document.getElementById("content");
    viderContainer(message);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                message.className = "alert alert-success";
                message.innerHTML = "La suppression a été réalisée avec " +
                    "succès!";
                 viderContainer(tableContainer);
            } else { // status = 404
                message.className = "alert alert-danger";
                message.innerHTML = "La suppression n'a pas pu être complétée.";
            }
        }
    };
    xhr.open("DELETE", "/api/declarations?du=" + dateDebut
        + '&au=' + dateFin + '&quartier=' + quartier, true);
    xhr.send();
}

/*
Envoie une requete ajax pour obtenir les declarations entre les deux dates et
le quartier si specifie. Creer un dictionnaire avec les valeurs a afficher.
 */
async function getDeclarationsByDates(dateDebut, dateFin, buttonId) {
    let tableContainer = document.getElementById("content");
    viderContainer(tableContainer);
    loadingAnimation(tableContainer);
    document.getElementById(buttonId).disabled = true;
    let quartier = document.getElementById("quartier");
    let response = await fetch('/api/declarations?du=' + dateDebut
        + '&au=' + dateFin, {method: "GET"});
    let content = await response.text();
    document.getElementById(buttonId).disabled = false;
    content = JSON.parse(content);
    let nbr_declarations = {};
    let quartiers = [];
    for (let i = 0; i < content.length; i++) { // on construit un dictionnaire avec le nbr de declarations par quartier
        nbr_declarations[content[i].nom_qr] =
                (nbr_declarations[content[i].nom_qr] || 0) + 1;
    }
    if (quartier.options[quartier.selectedIndex].value === "tous") {
        content.forEach((item) => {
            quartiers.push({ "Nom de l'arrondissement": item.nom_arr,
                    "Nom du quartier": item.nom_qr,
                    "Nombre de déclarations": nbr_declarations[item.nom_qr] });
        })
    } else {
        quartier = quartier.options[quartier.selectedIndex].value;
        content.forEach((item) => {
            if (item.nom_qr == quartier) {
                quartiers.push({ "Nom de l'arrondissement": item.nom_arr,
                    "Nom du quartier": item.nom_qr,
                    "Nombre de déclarations": nbr_declarations[item.nom_qr] });
            }
        })
    }
    return mapUniqueByKey(quartiers, "Nom du quartier");
}

/*
Permet de filter les declarations sans doublons
 */
function mapUniqueByKey(array, key) {
    return [...new Map(array.map((x) => [x[key], x])).values()];
}

/*
Creer une table a partir des donnes retournees par le backend
 */
function creerTable(jsonContent) {
    let header = trouverHeaderValues(jsonContent);
    let table = document.createElement('table');
    table.className = 'table-bordered table-hover';
    let tr = table.insertRow(-1);
    creerHeader(tr, header);
    creerBody(jsonContent, header, table);
    let container = document.getElementById("content");
    viderContainer(container);
    container.innerHTML = "";
    container.appendChild(table);
    document.getElementById("rechercher_qr").disabled = false;
}

/*
Trouve les en-tetes pour les headers de la table
 */
function trouverHeaderValues(jsonContent) {
    let header = [];
    for (let key in jsonContent[0]) {
        header.push(key);
    }
    return header;
}

/*
Creer le header de la table
 */
function creerHeader(tr, header) {
    for (let i = 0; i < header.length; i++) {
        let th = document.createElement('th');
        th.innerHTML = header[i];
        tr.appendChild(th);
    }
}

/*
Creer le body de la table
 */
function creerBody(jsonContent, header, table) {
    for (let i = 0; i < jsonContent.length; i++) {
        let tr = table.insertRow(-1);
        for (let j = 0; j < header.length; j++) {
            let td = tr.insertCell(-1);
            td.innerHTML = jsonContent[i][header[j]];
        }
    }
}

/*
Permet d'afficher une animation lors du loading d'une table
 */
function loadingAnimation(container) {
    for (let i = 0; i < 5; ++i) {
        div = document.createElement("div");
        div.className = "loading";
        container.appendChild(div);
    }
}

/*
Vide le tableau
 */
function viderContainer(container) {
    if (container.hasChildNodes()) {
        container.removeChild(container.firstChild);
    }
}

/*
Permet de valider les informations entrees par le nouvel utilisateur. Si valide,
envoie une requete pour ajouter cet utilisateur dans la base de donnees.
 */
function verifierInfoDeclarant() {
    let selectQuartier = document.getElementById("nom_quartier");
    let selectArrondissement =
            document.getElementById("nom_arrondissement");
    let quartier = selectQuartier.options[selectQuartier.selectedIndex].value;
    let arrondissement = selectArrondissement.options[selectArrondissement.
            selectedIndex].value;
    let adresse = document.getElementById("adresse").value;
    let dateVisite = document.getElementById("date_visite").value;
    let nom = document.getElementById("nom").value;
    let prenom = document.getElementById("prenom").value;
    let description = document.getElementById("description").value;
    let errorContainer = document.getElementById("error_declarant");
    if (dateVisite === "" || dateVisite == null || adresse === ""
            || adresse == null || nom === "" || nom == null || prenom === ""
            || prenom == null || description === "" || description == null) {
        errorContainer.innerHTML = "Tous les champs sont obligatoires.";
    } else if (!dateVisite.match(/(\d{4})-(\d{2})-(\d{2})/)) {
        errorContainer.innerHTML = "La date de visite n'a pas le bon format " +
                                    "(YYYY-MM-DD).";
    } else {
        errorContainer.innerHTML = "";
        envoyerDeclaration(quartier, arrondissement, adresse, dateVisite, nom,
                            prenom, description)
    }
}

/*
Envoie les informations d'une declaration interne au backend et affiche un
message de confirmation ou d'erreur selon le cas.
 */
function envoyerDeclaration(quartier, arrondissement, adresse, dateVisite, nom,
                            prenom, description) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                alert("Votre déclaration a bien été envoyée.");
                document.location.href = "/";
            } else {
                console.log("Erreur avec le serveur.");
            }
        }
    };
    xhr.open("POST", "/api/declaration", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
            "quartier": quartier, "arrondissement": arrondissement,
            "adresse": adresse, "dateVisite": dateVisite, "nom": nom,
            "prenom": prenom, "description": description
    }));
}

/*
Valider les informations entree par l'utilisateur lors de son inscription.
Envoie une requete au backend une fois validee pour enregistrer l'utilisateur
a la base de donnees.
 */
function validate_user() {
    let utilisateur = document.getElementById("new_username").value;
    let password = document.getElementById("new_password").value;
    let courriel = document.getElementById("new_email").value;
    let errorContainer = document.getElementById("error_user");
    let quartiers = document.getElementById("multiple_select_quartier").selectedOptions;
    let quartiers_names = Array.from(quartiers).map(({ value }) => value);
    if (utilisateur == null || utilisateur === "" ||
        password == null || password === "" || courriel == null ||
        courriel === ""){
        errorContainer.innerHTML = "Tous les champs doivent être remplis.";
    } else if (!courriel.match(/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/)){
        errorContainer.innerHTML = "Le courriel n'a pas un format valide.";
    } else if (quartiers_names.length === 0){
        errorContainer.innerHTML =
            "Veuillez choisir des quartiers à surveiller";
    } else { // tout est valide ici
        errorContainer.innerHTML = "";
        send_user_to_server(utilisateur, password, courriel, quartiers_names);
    }
}

/*
Envoie une requet ajax au backend contenant les informations du nouvel utilisa-
teur. Affiche un message de confirmation si bien ajoute.
 */
function send_user_to_server(utilisateur, password, courriel, quartiers) {
    // on va va d'abord recuperer les informations sur la liste des quartiers choisis
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                alert("Votre compte utilisateur a été créé avec succès.");
                document.location.href = "/login";
            } else {
                console.log("Erreur avec le serveur.");
            }
        }
    };
    xhr.open("POST", "/api/user", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
            "utilisateur": utilisateur, "mot_de_passe": password,
            "courriel": courriel, "quartiers_a_surveiller": quartiers.toString()
    }));
}

/*
Permet de disable un bouton lorsqu'une case n'est pas cochee. Utilisee sur la
page pour changer les quartiers surveilles par l'utilisateur.
 */
function enable_select(){
    document.getElementById("multiple_select_quartier").disabled =
        !document.getElementById("checkbox_disable_quartier").checked;
}

/*
Envoie une requete ajax afin de changer les quartiers surveilles par l'utilisa-
teur. Affiche un message de confirmation.
 */
function changer_quartiers_a_surveiller() {
    if (document.getElementById("checkbox_disable_quartier").checked) {
        let errorContainer = document.getElementById("error_quartier");
        let quartiers = document.getElementById("multiple_select_quartier").selectedOptions;
        let quartiers_names = Array.from(quartiers).map(({value}) => value);
        if (quartiers_names.length === 0)
            errorContainer.innerHTML = "Vous devez sélectionner des quartiers.";
            else {
            errorContainer.innerHTML = "";
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 201) {
                        alert("Les quartiers à surveiller ont été changés avec succès!");
                        document.location.href = "/modification";
                    } else
                        console.log("Erreur avec le serveur.");
                }
            };
            xhr.open("POST", "/modification", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify({"quartiers_a_surveiller": quartiers_names.toString()
            }));
        }
    }
}