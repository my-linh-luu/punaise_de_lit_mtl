function chercherParDates() {
    let dateDebut = document.getElementById("date_debut").value;
    let dateFin = document.getElementById("date_fin").value;
    if (dateDebut == null || dateDebut === "" || dateFin == null || dateFin === "") {
        document.getElementById("error_date").innerHTML = "Les deux dates doivent contenir une valeur.";
    } else if (!dateDebut.match(/(\d{4})-(\d{2})-(\d{2})/) 
                || !dateFin.match(/(\d{4})-(\d{2})-(\d{2})/)) {
        document.getElementById("error_date").innerHTML = "Les dates n'ont pas le bon format (YYYY-MM-DD).";
    } else { // ok, valide
        document.getElementById("error_date").innerHTML = "";
        chargerDeclarationEntreDates(dateDebut, dateFin);
    }
}

function chargerDeclarationEntreDates(dateDebut, dateFin) {
    let container = document.getElementById("content");
    getDeclarationsByDates(dateDebut, dateFin)
        .then(content => 
            container.innerHTML = content)
        .catch (error => 
            container.innerHTML = "<p>Erreur dans le chargement des données.</p>");
}


async function getDeclarationsByDates(dateDebut, dateFin) {
    let response = await fetch('/declarations?du=' + dateDebut + '&au=' + dateFin)
    let content = await response.text();
    return content;
}