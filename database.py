from re import split
import sqlite3


def build_dictionary(row):
    return {"NO_DECLARATION": row[0], "DATE_DECLARATION": row[1], "DATE_INSP_VISPRE": row[2],
            "NBR_EXTERMIN": row[3], "DATE_DEBUTTRAIT": row[4], "DATE_FINTRAIT": row[5],
            "No_QR": row[6], "NOM_QR": row[7], "NOM_ARROND": row[8], "COORD_X": row[9],
            "COORD_Y": row[10], "LONGITUDE": row[11], "LATITUDE": row[12], }

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

    def get_all_from_nom_qr(self, nom_qr):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from data where NOM_QR = ?"), (nom_qr,))
        results = cursor.fetchall()
        return [build_dictionary(row) for row in results]

    def get_all_from_nom_qr(self, nom_arr):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select * from data where NOM_ARROND = ?"), (nom_arr,))
        results = cursor.fetchall()
        return [build_dictionary(row) for row in results]
