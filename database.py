from re import split
import sqlite3
from datetime import datetime
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

    def get_all_by_nom_qr_or_nom_arr(self, nom):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from data where NOM_QR like ? or NOM_ARROND like ? order by DATE_DECLARATION desc"), ("%"+nom+"%", "%"+nom+"%",))  # like permet de faire une recherche case insensitive
        declarations = cursor.fetchall()
        return [Declaration(declaration[0], declaration[1], declaration[2], declaration[3], declaration[4], declaration[5],
                            declaration[6], declaration[7], declaration[8], declaration[9], declaration[10], declaration[11],
                            declaration[12]) for declaration in declarations]

    def get_all_in_between_dates(self, debut, fin):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from data where DATE_DECLARATION <= ? and DATE_DECLARATION >= ? order by DATE_DECLARATION desc"),
            (datetime.strptime(fin,'%Y-%m-%d'), datetime.strptime(debut,'%Y-%m-%d'),))
        declarations = cursor.fetchall()
        return [Declaration(declaration[0], declaration[1], declaration[2], declaration[3], declaration[4], declaration[5],
                            declaration[6], declaration[7], declaration[8], declaration[9], declaration[10], declaration[11],
                            declaration[12]) for declaration in declarations]

    def get_nbr_declaration_par_quartier(self, nom_qr, debut, fin):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select COUNT() from data where NOM_QR = ? and DATE_DECLARATION <= ? and DATE_DECLARATION >= ?"),
            (nom_qr, datetime.strptime(fin, '%Y-%m-%d'), datetime.strptime(debut, '%Y-%m-%d'),))
        compte = cursor.fetchone()
        return compte[0]

    def get_quartiers(self, debut, fin):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select distinct NOM_QR from data where DATE_DECLARATION <= ? and DATE_DECLARATION >= ?"),
            (datetime.strptime(fin, '%Y-%m-%d'), datetime.strptime(debut, '%Y-%m-%d'),))
        quartiers = cursor.fetchall()
        return [quartier for quartier in quartiers]
