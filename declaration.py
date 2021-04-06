class Declaration :
    def __init__(self, noDeclaration, dateDeclaration, dateInspVispre,
                nbrExtermin, dateDebutTrait, dateFinTrait, noQr, nomQr, nomArr,
                coorX, coorY, long, lat):
        self.noDeclaration = noDeclaration
        self.dateDeclaration = dateDeclaration
        self.dateInspVispre = dateInspVispre
        self.nbrExtermin = nbrExtermin
        self.dateDebutTrait = dateDebutTrait
        self.dateFinTrait = dateFinTrait
        self.noQr = noQr;
        self.nomQr = nomQr;
        self.nomArr = nomArr;
        self.coorX = coorX;
        self.coorY = coorY;
        self.long = long;
        self.lat = lat;


    def build_dictionary(self):
        return {"NO_DECLARATION": self.noDeclaration, "DATE_DECLARATION": self.dateDeclaration, "DATE_INSP_VISPRE": self.dateInspVispre,
                "NBR_EXTERMIN": self.nbrExtermin, "DATE_DEBUTTRAIT": self.dateDebutTrait, "DATE_FINTRAIT": self.dateFinTrait,
                "No_QR": self.noQr, "NOM_QR": self.nomQr, "NOM_ARROND": self.nomArr, "COORD_X": self.coorX,
                "COORD_Y": self.coorY, "LONGITUDE": self.long, "LATITUDE": self.lat}
