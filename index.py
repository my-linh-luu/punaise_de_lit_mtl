from flask import Flask, render_template, request, redirect, g, \
    jsonify, make_response, Response, session
from flask.helpers import url_for
from apscheduler.schedulers.background import BackgroundScheduler
from flask_json_schema import JsonValidationError, JsonSchema
from io import StringIO
from functools import wraps
import requests
import pandas as pd
import hashlib
import uuid
import datetime
import re

from .db.database import Database
from .doc.schemas import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
schema = JsonSchema(app)
scheduler = BackgroundScheduler()


# Permet d'accéder à notre base de donnees
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


# Affiche un message d'erreur lorsque les donnees ne respectent pas le
# jsonschema defini
@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400


# Permet de récupérer les nouvelles données à chaque jour à minuit
@scheduler.scheduled_job('cron', hour=0)
def fetch_data_periodically():
    with app.app_context():
        csv_url = ('https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a'
                   '-fca82d4f5c2f/resource/6173de60-c2da-4d63-bc75'
                   '-0607cb8dcb74/download/declarations-exterminations'
                   '-punaises-de-lit.csv')
        s = requests.get(csv_url).content
        df = pd.read_csv(StringIO(s.decode('utf-8')))
        print("fetching...")
        index = len(df.index)
        for i in range(index):
            no_declaration = str(df.iloc[i][0]).strip()
            date_declaration = df.iloc[i][1]
            date_insp_vispre = df.iloc[i][2]
            nbr_extermin = df.iloc[i][3]
            date_debuttrait = df.iloc[i][4]
            date_fintrait = df.iloc[i][5]
            n_qr = df.iloc[i][6]
            nom_qr = df.iloc[i][7]
            nom_arrond = df.iloc[i][8]
            coord_x = df.iloc[i][9]
            coord_y = df.iloc[i][10]
            longitude = df.iloc[i][11]
            latitude = df.iloc[i][12]
            # verification pour les elements supprimes
            no_declaration_supprimee = get_db().get_no_declaration_supprimee(
                no_declaration)
            if no_declaration_supprimee is not None:
                continue
            # verification pour les doublons
            verification = get_db().get_declaration_by_no_declaration(
                no_declaration)
            if verification is None:
                get_db().add_declaration_externe(no_declaration,
                                                 date_declaration,
                                                 date_insp_vispre,
                                                 nbr_extermin, date_debuttrait,
                                                 date_fintrait, n_qr, nom_qr,
                                                 nom_arrond, coord_x, coord_y,
                                                 longitude, latitude)
        print("Base de données à jour.")


scheduler.start()


# Redirige vers la page HTML du RAML
@app.route("/doc")
def get_doc():
    return render_template("doc.html")


# Redirige vers la page d'accueil et s'occupe de rediriger la recherche
# dans la barre d'accueil principale
@app.route("/", methods=["GET", "POST"])
def accueil():
    quartiers = get_db().get_distinct_quartiers()
    if request.method == "GET":
        return render_template("accueil.html", quartiers=quartiers,
                               session=session)
    else:
        recherche = request.form["recherche"]
        quartiers = get_db().get_distinct_quartiers()
        if recherche == "":
            return render_template("accueil.html",
                                   error="Veuillez entrer une valeur.",
                                   quartiers=quartiers, session=session)
        else:  # utilisateur a entrer quelque chose dans la barre de rech
            resultats = get_db().get_declarations_by_qr_arr(recherche)
            if not resultats:  # si dictionnaire est vide, affiche false et
                # ne rentrera pas dans cette condition
                return render_template("accueil.html",
                                       error="Aucun résultat correspondant"
                                             " à votre recherche.",
                                       quartiers=quartiers,
                                       session=session)
        return redirect(url_for('get_declarations_by_qr_arr',
                                recherche=recherche))


# Redirige vers la page contenant les résultats de la recherche des
# declarations par nom de quartier ou arrondissement
@app.route("/resultats/<recherche>")
def get_declarations_by_qr_arr(recherche):
    resultats = get_db().get_declarations_by_qr_arr(recherche)
    return render_template("recherche.html", recherche=resultats)


# Redirige vers la page pour ajouter une declaratin
@app.route("/declaration", methods=["GET"])
def ajouter_declaration():
    quartiers = get_db().get_distinct_quartiers()
    arrondissements = get_db().get_distinct_arrondissements()
    return render_template("ajouter.html", quartiers=quartiers,
                           arrondissements=arrondissements)


# service REST pour obtenir les déclarations entre deux dates
@app.route("/api/declarations", methods=["GET"])
def get_declarations_by_dates():
    if request.method == "GET":
        date_debut = request.args.get('du')
        date_fin = request.args.get('au')
        declarations = get_db().get_declarations_in_between_dates(date_debut,
                                                                  date_fin)
        return jsonify(
            [declaration.asDictionary() for declaration in declarations])


# service REST pour supprimer les déclarations d'un quartier
@app.route("/api/declarations", methods=["DELETE"])
def delete_declarations():
    date_debut = request.args.get('du')
    date_fin = request.args.get('au')
    quartier = request.args.get('quartier')
    declarations = get_db().get_declarations_in_between_dates_by_quartier(
        date_debut, date_fin, quartier)
    if not declarations:
        return "", 404
    else:
        for declaration in declarations:
            get_db().add_no_declaration_supprimee(
                declaration.no_declaration)
            get_db().delete_declarations_by_quartier(date_debut, date_fin,
                                                     quartier)
        return "", 200


# service REST pour créer une déclaration à l'interne
@app.route("/api/declaration", methods=["POST"])
@schema.validate(declaration_insert_schema)
def create_declaration():
    declaration = request.get_json()
    if declaration["quartier"] == "" \
            or declaration["arrondissement"] == "" \
            or declaration["adresse"] == "" \
            or declaration["dateVisite"] == "" \
            or declaration["nom"] == "" or declaration["prenom"] == "" \
            or declaration["description"] == "":
        return render_template("ajouter.html",
                               error="Tous les champs sont obligatoires.")
    else:
        try:
            datetime.datetime.strptime(declaration["dateVisite"], '%Y-%m-%d')
        except ValueError:
            return render_template("ajouter.html",
                                   error="La date de visite n'a pas "
                                         "le bon format (YYYY-MM-DD).")
    id = get_db().add_declaration(declaration["quartier"],
                                  declaration["arrondissement"],
                                  declaration["adresse"],
                                  declaration["dateVisite"],
                                  declaration["nom"], declaration["prenom"],
                                  declaration["description"])
    return jsonify(get_db().get_one_declaration(id)), 201


# service REST pour supprimer une déclaration à l'interne ayant un id
# spécifique
@app.route("/api/declaration/<id>", methods=["DELETE"])
def delete_declaration(id):
    declaration = get_db().get_one_declaration(id)
    if declaration is None:
        return "", 404
    else:
        get_db().delete_one_declaration(id)
        return "", 200


# service REST pour afficher tous les quartiers avec le nombre de déclarations
# dans ce quartier
@app.route("/api/declarations/quartiers", methods=["GET"])
def get_count_by_quartier():
    dic_quartiers = dict()
    array_quartiers = []
    quartiers = get_db().get_quartiers()
    for quartier in quartiers:
        if quartier in dic_quartiers:
            continue
        else:
            compte = quartiers.count(quartier)
            dic_quartiers[quartier] = compte
    uniques = dict(sorted(dic_quartiers.items(), key=lambda item: item[1],
                          reverse=True))
    for key, value in uniques.items():
        array_quartiers.append({"Nom du quartier": key,
                                "Nombre de déclarations": value})
    return jsonify(array_quartiers)


# Permet de rediriger vers la page pour se login
@app.route("/login", methods=["GET"])
def load_login_page():
    return render_template("login.html")


# Permet de valider si les informations de l'utilisateur correspondent à celles
# dans la base de données. Si oui, login avec succes et l'utilisateur et
# redirigé.
@app.route("/login", methods=["POST"])
def login_page():
    username = request.form["username"]
    password = request.form["mot_de_passe"]
    if username == "" or password == "":
        return render_template("login.html",
                               error="Tous les champs sont obligatoires")
    # tous les champs sont valides, il faut verifier si le user existe
    user = get_db().get_user_login_info(username)
    if user is None:
        return render_template("login.html",
                               error="Ce nom d'utilisateur n'existe pas.")
    salt = user[0]
    hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")) \
        .hexdigest()
    if hashed_password == user[1]:
        # OK acces autorisé on cree la session et on redirige
        id_session = uuid.uuid4().hex
        session["id"] = id_session
        get_db().save_session(id_session, username)
        return redirect("/")
    else:  # le password ne correspond pas
        return render_template("login.html",
                               error="Le mot de passe ne correspond pas "
                                     "avec cet utilisateur.")


# Permet de rediriger vers la page pour s'inscrire en tant que nouvel
# utilisateur
@app.route("/new_user", methods=["GET"])
def new_user():
    quartiers = get_db().get_distinct_quartiers()
    return render_template("creer_profil.html", quartiers=quartiers)


# Permet de valider les informations entrees par le nouvel utilisateur.
# Si valide, l'utilisateur est enregistré dans la base de données et est
# redirigé vers la page de login.
@app.route("/api/user", methods=["POST"])
@schema.validate(user_insert_schema)
def create_user():
    pattern = "[^@]+@[^@]+.[^@]+"
    user = request.get_json()
    if user["utilisateur"] == "" or user["mot_de_passe"] == "" \
            or user["courriel"] == "":
        return render_template("creer_profil.html",
                               error="Tous les champs doivent être remplis."
                               )
    if not re.match(pattern, user["courriel"]):
        return render_template("creer_profil.html",
                               error="Le courriel n'a pas le bon format.")
    if user["quartiers_a_surveiller"].find("tous") != -1 \
            and user["quartiers_a_surveiller"].find(",") != -1:
        return render_template("creer_profil.html",
                               error="L'option \"Tous les quartiers\" ne "
                                     "peut être choisi avec d'autres "
                                     "quartiers.")
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(
        str(user["mot_de_passe"] + salt).encode("utf-8")).hexdigest()
    id = get_db().add_user(user["utilisateur"], hashed_password,
                           user["courriel"],
                           user["quartiers_a_surveiller"], salt)
    return jsonify(get_db().get_user(id)), 201


# Permet de valider que l'utilisateur s'est bien authentifié pour pouvoir
# accéder à la page
def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)

    return decorated


# Permet de rediriger vers la page qui permet à l'utilisateur de changer les
# quartiers qu'il surveille. Apporte le changement à la base de données pour
# cet utilisateur.
@app.route('/modification', methods=["GET", "POST"])
@authentication_required
def modifier_user():
    id_session = session["id"]
    quartiers = get_db().get_distinct_quartiers()
    username = get_db().get_session(id_session)
    quartiers_surveilles = get_db().get_quartiers_surveilles(username)
    if request.method == "GET":
        return render_template("user_page.html", quartiers=quartiers,
                               username=username,
                               quartiers_surveilles=quartiers_surveilles)
    else:  # POST
        user = request.get_json()
        quartiers = user["quartiers_a_surveiller"]
        get_db().replace_quartiers(quartiers, username)
        return Response(status=201)


# Permet de rediriger vers la page pour ajouter une photo de profil. Si une
# photo de profil existe deja pour cet utilisateur, va l'afficher
@app.route('/upload_photo', methods=["GET"])
@authentication_required
def load_page_photo():
    id_session = session["id"]
    username = get_db().get_session(id_session)
    if request.method == "GET":
        # verifier s'il ny a pas deja une photo de profil, si oui afficher
        pic_id = get_db().get_picture_id(username)
        if pic_id is None:  # pas de photo a son profil
            return render_template("picture_form.html")
        else:
            return render_template("picture_form.html", picture_id=pic_id)


# Permet d'ajouter une photo de profil à l'utilisateur, la photo sera
# enregistree dans la base de donnees et elle sera affichee sur la meme page
@app.route('/upload_photo', methods=["POST"])
@authentication_required
def ajouter_photo():
    id_session = session["id"]
    username = get_db().get_session(id_session)
    photo = None
    picture_id = None
    if "photo" in request.files:
        photo = request.files["photo"]
        picture_id = str(uuid.uuid4().hex)
    if photo.filename == '':  # pas de photo soumise
        pic_id = get_db().get_picture_id(username)
        if pic_id is None:  # pas de photo prealablement affichee
            return render_template("picture_form.html",
                                   error="Vous devez sélectionner une "
                                         "image.")
        return render_template("picture_form.html", picture_id=pic_id,
                               error="Vous devez sélectionner une image.")
    else:
        get_db().add_picture(picture_id, username)
        get_db().create_picture(picture_id, photo)
    return render_template("picture_form.html", picture_id=picture_id)


# Permet d'afficher chargee l'image sur la page
@app.route('/image/<pic_id>.png')
def download_picture(pic_id):
    binary_data = get_db().load_picture(pic_id)
    if binary_data is None:
        return Response(status=404)
    else:
        response = make_response(binary_data)
        response.headers.set('Content-Type', 'image/png')
    return response


# Permet à l'utilisateur de se deconnecter
@app.route('/logout', methods=["GET"])
@authentication_required
def logout():
    id_session = session["id"]
    session.pop('id', None)
    get_db().delete_session(id_session)
    return redirect("/")


# Verifie si l'utilisateur est authentifie
def is_authenticated(session):
    return "id" in session


# Affiche un message d'erreur si l'utilisateur essaie de rentrer sur une page
# qui necessite une authentification
def send_unauthorized():
    return make_response('Could not verify your access level for that URL.\n'
                         'You have to login with the proper credentials.', 401,
                         {'WWW-Authenticate': 'Basic realm="Login Required"'})


app.secret_key = "jf43jihr)8^@#32n+#(;s5ad7"
