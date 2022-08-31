from .utils import Utils
import sqlite3 as sqlite3
from sqlite3 import Error
import pandas as pd
from libraries.html import HtmlFactory


class Sqlite3Wrap(object):

    @classmethod
    def initConn(cls, db_file):
        try:
            conn = sqlite3.connect(db_file)
            message = "connexion reuissi"
            return conn

        except sqlite3.Error as error:
            print("Erreur de connexion a SQLite", error)

        return conn


    @classmethod
    def create_table(cls, instanceDB, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            #c = cls.initConn("pythonsqlite.db")
            c = instanceDB.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)


    @classmethod
    def select_rows(cls, conn, sqlQuery):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        #sqlQuery = "SELECT * FROM personel"
        cur.execute(sqlQuery)

        rows = cur.fetchall()

        # for row in rows:
        #     print(row)
        return rows

    @classmethod
    def write_to_db(cls, conn, df:pd.DataFrame, tableName):
        # write the dataframe into the DB
        cur = conn.cursor()
        df.to_sql(tableName, conn, if_exists='replace', index=False)

        return df


    @classmethod
    def main(cls):
        #data = cls.initConn("pythonsqlite.db")

        sql_create_personel_table = """ CREATE TABLE IF NOT EXISTS personel (
                                               id integer PRIMARY KEY,
                                               name text,
                                               phone text,
                                               email text,
                                               address text,
                                               latlng text,
                                               salary float,
                                               age int
                                           ); """
        conn = cls.initConn("pythonsqlite.db")

        # Recupration de la dataFrame de HtmlFactory
        df = HtmlFactory.main()

        # Sauvegarde de la donne dans la BDD Sqlite
        data = cls.write_to_db(conn,df,'personel')
        # if data:
        #     data = "Sauvergarde reussi"
        data = cls.select_rows(conn,sqlQuery="SELECT * FROM personel")

        return data
