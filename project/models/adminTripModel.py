# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminTripModel(object):

    # Add Trip Data
    def addTripData(self, destination, country):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO trip(destination, country) VALUES(%s,%s)", (destination, country))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Fetch All Trip Data
    def tripFetchData(self):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("SELECT * FROM trip")

        vendor_data = cur.fetchall()

        return vendor_data

    # Fetch One Trip Data
    def tripDataFetchOne(self, id):

        # fill the form from database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get article id
        cur.execute("SELECT * FROM trip WHERE trip_id = %s", [id])

        trip_data = cur.fetchone()
        cur.close()

        return trip_data

    # Update Trip Data
    def updateTripData(self, destination, country, trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("UPDATE trip SET destination=%s, country=%s WHERE trip_id=%s", (destination, country, trip_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Delete Trip Data
    def deleteTripData(self, trip_id):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("DELETE FROM trip WHERE trip_id = %s", [trip_id])

        # Commit to DB
        mysql.connection.commit()

        # Close
        cur.close()

    # Fetch Country Data
    def countryFetchData(self):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("SELECT DISTINCT country FROM trip")

        # asign to the variable
        country_data = cur.fetchall()

        # Close
        cur.close()

        return country_data

    # Fetch One Country Data Chosen
    def countryFetchOneData(self, country):

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute('''
            SELECT country FROM trip
            WHERE country = %s
        ''', [country])

        # Asign to the variable
        country_data_fetch_one = cur.fetchone()

        # Close the DB
        cur.close()

        # Return the value
        return country_data_fetch_one

    # Fetch Destination Data
    def destinationFetchOne(self, country):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute('''
            SELECT destination FROM trip
            WHERE country = %s
        ''', [country])

        # Asign to the variable
        destination_data = cur.fetchall()

        # Close
        cur.close()

        # return the data
        return destination_data

    # Fetch Destination Data from Trip ID
    def destinationFetchOneFromTripId(self, trip_id):

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute('''
            SELECT destination FROM trip
            WHERE trip_id = %s
        ''', [trip_id])

        # Asign to the variable
        destination = cur.fetchone()

        # Close
        cur.close()

        # return the data
        return destination

    # Fetch Trip ID from Destination
    def tripIdFetchOneFromDestination(self, destination):

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute('''
            SELECT trip_id FROM trip
            WHERE destination = %s
        ''', [destination])

        # Asign to the variable
        trip_id = cur.fetchone()

        # Close
        cur.close()

        # return the data
        return trip_id
