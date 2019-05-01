# -*- coding: utf-8 -*-
from flask import Flask
from project import mysql

class indexModel(object):

    # fetch the trip data
    def tripFetchData(self):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("SELECT * FROM trip")

        trip_data = cur.fetchall()

        return trip_data
