from re import split
import sqlite3
from .declaration import Declaration

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

    def search_by_nom_qr_or_nom_arr(self, nom):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from data where NOM_QR like ? or NOM_ARROND like ?"), ("%"+nom+"%", "%"+nom+"%",))  # like permet de faire une recherche case insensitive
        declarations = cursor.fetchall()
        return [Declaration(declaration[0], declaration[1], declaration[2], declaration[3], declaration[4], declaration[5],
                            declaration[6], declaration[7], declaration[8], declaration[9], declaration[10], declaration[11],
                            declaration[12]) for declaration in declarations]
