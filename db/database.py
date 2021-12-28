import sqlite3
from datetime import datetime
from ..declaration import Declaration


# Cette classe définie les fonctions qui permettent d'accéder à la base de
# données


class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/data.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # Permet d'ajouter une declaration de la ville a la base de donnee
    def add_declaration_externe(self, no_declaration, date_declaration,
                                date_insp_vispre, nbr_extermin, date_debut,
                                date_fin, no_qr, nom_qr, nom_arrond, coor_x,
                                coor_y, longitude, latitude):
        connection = self.get_connection()
        connection.execute(
            ("insert into declarations_ville(NO_DECLARATION, DATE_DECLARATION,"
             "DATE_INSP_VISPRE, NBR_EXTERMIN, DATE_DEBUTTRAIT, DATE_FINTRAIT,"
             "No_QR, NOM_QR, NOM_ARROND, COORD_X, COORD_Y, LONGITUDE,"
             "LATITUDE)"
             " values(?,?,?,?,?,?,?,?,?,?,?,?,?)"), (no_declaration,
                                                     date_declaration,
                                                     date_insp_vispre,
                                                     nbr_extermin, date_debut,
                                                     date_fin, no_qr, nom_qr,
                                                     nom_arrond, coor_x,
                                                     coor_y, longitude,
                                                     latitude,))
        connection.commit()

    # Permet d'obtenir les declarations de la ville selon le nom
    # d'arrondissement ou le nom de quartier classer en ordre decroissant
    # des dates de declarations
    def get_declarations_by_qr_arr(self, nom):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from declarations_ville where NOM_QR like ? "
             "or NOM_ARROND like ? order by DATE_DECLARATION desc"),
            ("%" + nom + "%", "%" + nom + "%",))
        declarations = cursor.fetchall()
        return [Declaration(declaration[0], declaration[1], declaration[2],
                            declaration[3], declaration[4], declaration[5],
                            declaration[6], declaration[7], declaration[8],
                            declaration[9], declaration[10], declaration[11],
                            declaration[12], declaration[13]) for declaration
                in declarations]

    # Permet d'obtenir les declarations de la ville entre deux dates et
    # classe en ordre croissant selon la date de declaration
    def get_declarations_in_between_dates(self, debut, fin):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from declarations_ville where DATE_DECLARATION <= ? "
             "and DATE_DECLARATION >= ? order by DATE_DECLARATION"),
            (datetime.strptime(fin, '%Y-%m-%d'),
             datetime.strptime(debut, '%Y-%m-%d'),))
        declarations = cursor.fetchall()
        return [Declaration(declaration[0], declaration[1], declaration[2],
                            declaration[3], declaration[4], declaration[5],
                            declaration[6], declaration[7], declaration[8],
                            declaration[9], declaration[10], declaration[11],
                            declaration[12], declaration[13])
                for declaration in declarations]

    # Permet d'obtenir les declarations de la ville entre deux dates par
    # quartier et classe par nom de quartier
    def get_declarations_in_between_dates_by_quartier(self, debut, fin,
                                                      quartier):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from declarations_ville where DATE_DECLARATION <= ? "
             "and DATE_DECLARATION >= ? and NOM_QR = ? "
             "order by NOM_QR"),
            (datetime.strptime(fin, '%Y-%m-%d'),
             datetime.strptime(debut, '%Y-%m-%d'), quartier))
        declarations = cursor.fetchall()
        return [Declaration(declaration[0], declaration[1], declaration[2],
                            declaration[3], declaration[4], declaration[5],
                            declaration[6], declaration[7], declaration[8],
                            declaration[9], declaration[10], declaration[11],
                            declaration[12], declaration[13])
                for declaration in declarations]

    # Permet d'obtenir tous les quartiers noms des quartiers avec doublon
    def get_quartiers(self):
        cursor = self.get_connection().cursor()
        cursor.execute(("select NOM_QR from declarations_ville"))
        quartiers = cursor.fetchall()
        return [quartier[0] for quartier in quartiers]

    # Permet d'obtenir une declaration specifie par le numero de declaration
    def get_declaration_by_no_declaration(self, numero):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from declarations_ville where NO_DECLARATION = ?"),
            (numero,))
        declaration = cursor.fetchone()
        return declaration

    # Permet d'obtenir les noms des quartiers sans doublon
    def get_distinct_quartiers(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select distinct NOM_QR from declarations_ville order by NOM_QR"))
        quartiers = cursor.fetchall()
        return [quartier[0] for quartier in quartiers]

    def get_distinct_arrondissements(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select distinct NOM_ARROND from declarations_ville where "
             "NOM_ARROND is not NULL order by NOM_ARROND"))
        arrondissements = cursor.fetchall()
        return [arrondissement[0] for arrondissement in arrondissements]

    # Permet de supprimer les declarations d'un quartier specifique entre deux
    # dates
    def delete_declarations_by_quartier(self, debut, fin, quartier):
        connection = self.get_connection()
        connection.execute(
            ("delete from declarations_ville where NOM_QR = ? and"
             " DATE_DECLARATION <= ? and DATE_DECLARATION >= ?"),
            (quartier, datetime.strptime(fin, '%Y-%m-%d'),
             datetime.strptime(debut, '%Y-%m-%d'),))
        connection.commit()

    # DEBUT DES FONCTIONS POUR LA TABLE DES DECLARATIONS INTERNES

    # Permet d'ajouter une declaration a l'interne et retourne l'id associe
    # a cette declaration
    def add_declaration(self, nom_qr, nom_arr, adresse, date_visite, nom,
                        prenom, description):
        connection = self.get_connection()
        connection.execute("insert into declarations_internes(nom_quartier"
                           ",nom_arrondissement, adresse, date_visite, "
                           "nom_resident, prenom_resident, description)"
                           "values(?,?,?,?,?,?,?)", (nom_qr, nom_arr, adresse,
                                                     date_visite, nom, prenom,
                                                     description,))
        connection.commit()

        cursor = connection.cursor()
        cursor.execute("select last_insert_rowid()")
        result = cursor.fetchall()
        return result[0][0]  # retourne l'id de la declaration

    # Permet d'obtenir une declaration associee a l'id
    def get_one_declaration(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from declarations_internes where id = ?"),
                       (id,))
        declaration = cursor.fetchone()
        if declaration is not None:
            return {"id": declaration[0], "nom_quartier": declaration[1],
                    "nom_arrondissement": declaration[2],
                    "adresse": declaration[3], "date_visite": declaration[4],
                    "nom_resident": declaration[5],
                    "prenom_resident": declaration[6],
                    "description": declaration[7]}
        else:
            return declaration

    # Permet de supprimer une declaration selon son identifiant
    def delete_one_declaration(self, id):
        connection = self.get_connection()
        connection.execute(("delete from declarations_internes where id = ?"),
                           (id,))
        connection.commit()

    # FONCTION POUR GARDER NUMEROS DES DECLARATIONS DE LA VILLE SUPPRIMEES DANS
    # UNE TABLE

    # Permet d'ajouter le numero de declaration aux declarations supprimees
    def add_no_declaration_supprimee(self, numero):
        connection = self.get_connection()
        connection.execute(
            ("insert into declarations_supprimees values(?)"),
            (numero,))
        connection.commit()

    # Permet d'obtenir le numero de la declaration supprimee si elle a ete
    # supprimee
    def get_no_declaration_supprimee(self, numero):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from declarations_supprimees where no_declaration = ?"),
            (numero,))
        declaration = cursor.fetchone()
        return declaration

    # FONCTIONS POUR AJOUTER UN UTILISATEUR DANS LA BASE DE DONNÉES

    # Permet d'ajouter un utilisateur a la base de donnees et retourne l'id
    # associe a cet utilisateur
    def add_user(self, utilisateur, hpassword, courriel, quartiers, salt):
        connection = self.get_connection()
        connection.execute(
            ("insert into users(utilisateur, hashed_password, courriel,"
             "quartiers_a_surveiller, salt) values(?,?,?,?,?)"),
            (utilisateur, hpassword, courriel, quartiers, salt,))
        connection.commit()

        cursor = connection.cursor()
        cursor.execute("select last_insert_rowid()")
        result = cursor.fetchall()
        return result[0][0]  # retourne l'id de l'utilisateur

    # Permet d'obtenir et salt et le mot de passe hache de l'utilisateur
    def get_user_login_info(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute(("select salt, hashed_password from users where "
                        "utilisateur = ?"), (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]

    # Retourne l'utilisateur associe a l'id
    def get_user(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from users where id=?"), (id,))
        user = cursor.fetchone()
        return {"id": user[0], "utilisateur": user[1],
                "hashed_password": user[2], "courriel": user[3],
                "quartiers_a_surveiller": user[4], "salt": user[5],
                "pic_id": user[6]}

    # Retourne la liste des quartiers surveilles par l'utilisateur
    def get_quartiers_surveilles(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute(("select quartiers_a_surveiller from users where "
                        "utilisateur = ?"), (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0]

    # Permet de remplacer les quartiers surveilles par l'utilisateur
    def replace_quartiers(self, quartiers, username):
        connection = self.get_connection()
        connection.execute(("update users set quartiers_a_surveiller = ? "
                            "where utilisateur = ?"), (quartiers, username))
        connection.commit()

    # FONCTION POUR LA TABLE PICTURES

    # Permet d'ajouter un identifiant de photo a un utilisateur
    def add_picture(self, picture_id, username):
        connection = self.get_connection()
        connection.execute(("update users set pic_id = ? "
                            "where utilisateur = ?"), (picture_id, username))
        connection.commit()

    # Permet d'ajouter une photo associee a un identifiant dans la base de
    # donnees
    def create_picture(self, picture_id, file_data):
        connection = self.get_connection()
        connection.execute(("insert into pictures values(?,?)"),
                           (picture_id, sqlite3.Binary(file_data.read())))
        connection.commit()

    # Permet d'obtenir l'identifiant de la photo associe a cet utilisateur
    def get_picture_id(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select pic_id from users where utilisateur = ?"), (username,))
        pic_id = cursor.fetchone()
        if pic_id is None:
            return None
        else:
            return pic_id[0]

    # Permet d'obtenir le fichier binaire de la photo associee a l'identifiant
    def load_picture(self, picture_id):
        cursor = self.get_connection().cursor()
        cursor.execute(("select data from pictures where id = ?"),
                       (picture_id,))
        picture = cursor.fetchone()
        if picture is None:
            return None
        else:
            blob_data = picture[0]
            return blob_data

    # FONCTION POUR LA TABLE SESSION

    # Sauvegarde la session dans la base de donnees
    def save_session(self, id_session, utilisateur):
        connection = self.get_connection()
        connection.execute(("insert into session(id_session, utilisateur)"
                            "values(?,?)"), (id_session, utilisateur))
        connection.commit()

    # Supprime la session dans la base de donnees
    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("delete from session where id_session = ?"),
                           (id_session,))
        connection.commit()

    # Permet d'obtenir l'identifiant de l'utilisateur associe a une session
    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("select utilisateur from session where id_session=?"),
                       (id_session,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]
