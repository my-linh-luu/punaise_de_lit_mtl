# Classe qui permet de définir tous les attributs d'une déclaration provenant
# de la ville


class Declaration:
    def __init__(self, id, no_declaration, date_declaration, date_insp_vispre,
                 nbr_extermin, date_debut_trait, date_fin_trait, no_qr, nom_qr,
                 nom_arr,
                 coord_x, coord_y, longitude, latitude):
        self.id = id
        self.no_declaration = no_declaration
        self.date_declaration = date_declaration
        self.date_insp_vispre = date_insp_vispre
        self.nbr_extermin = nbr_extermin
        self.date_debut_trait = date_debut_trait
        self.date_fin_trait = date_fin_trait
        self.no_qr = no_qr
        self.nom_qr = nom_qr
        self.nom_arr = nom_arr
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.longitude = longitude
        self.latitude = latitude

    # transforme en dictionnaire une declaration
    def asDictionary(self):
        return {
            "id": self.id,
            "no_declaration": self.no_declaration,
            "date_declaration": self.date_declaration,
            "date_insp_vispre": self.date_insp_vispre,
            "nbr_extermin": self.nbr_extermin,
            "date_debut_trait": self.date_debut_trait,
            "date_fin_trait": self.date_fin_trait,
            "no_qr": self.no_qr,
            "nom_qr": self.nom_qr,
            "nom_arr": self.nom_arr,
            "coord_x": self.coord_x,
            "coord_y": self.coord_y,
            "longitude": self.longitude,
            "latitude": self.latitude}
