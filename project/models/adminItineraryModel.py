# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminItineraryModel(object):

    # Add the Itinerary Data to the Database
    def addItinerary(self, day_no, package_trip_id, airpor_transfer_title, airpor_transfer_description):

        # create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT INTO itinerary
            (day_no, package_trip_id, itinerary_title, itinerary_detail)
            VALUES (%s, %s, %s, %s)
        ''', (day_no, package_trip_id, airpor_transfer_title, airpor_transfer_description))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()


    # Fetch the last update from the table
    def lastUpdateItinerary(self):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT * FROM itinerary
            WHERE time_stamp = (SELECT MAX(time_stamp) FROM itinerary)
        ''')

        itinerary_data = cur.fetchone()

        # Close the connection
        cur.close()

        # Return the variable
        return itinerary_data

    # Fetch the itinerary for the Package Trip Data
    def itineraryFetchData(self, package_trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `itinerary`.`day_no`
        ''')
