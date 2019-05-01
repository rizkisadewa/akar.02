# -*- coding: utf-8 -*-
from flask import Flask
from project import mysql

class clientServicesModel(object):

    # Fetch the Services Refer to the Trip ID
    def clientServicesFetchData(self, trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT * FROM services
            WHERE trip_id = %s
        ''', [trip_id])

        # Asign to the variable
        service_data = cur.fetchall()

        # close the connection
        cur.close()

        return service_data

    # Fetch the Destinations Data
    def destinationFetchData(self):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # execute query
        cur.execute('''
            SELECT destination FROM trip
        ''')

        # Asign to the variable
        destiation_data = cur.fetchall()

        # close the connection
        cur.close()

        return destiation_data
