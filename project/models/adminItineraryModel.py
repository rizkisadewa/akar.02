# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminItineraryModel(object):

    # Add the Itinerary Data to the Database
    def addItinerary(self, day_no, package_trip_id, itinerary_title, itinerary_detail, type):

        # create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT INTO itinerary
            (day_no, package_trip_id, itinerary_title, itinerary_detail, type)
            VALUES (%s, %s, %s, %s, %s)
        ''', (day_no, package_trip_id, itinerary_title, itinerary_detail, type))

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
            *
            FROM `itinerary`
            WHERE `itinerary`.`package_trip_id` = %s
        ''', [package_trip_id])

        # Asign to the variable
        itinerary_data = cur.fetchall()

        # Close the connection
        cur.close()

        # return the variable
        return itinerary_data

    # Fetch the itinerary refer to itinerary ID
    def itineraryFetchDataFromId(self, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            *
            FROM itinerary
            WHERE itinerary_id = %s
        ''', [itinerary_id])

        # Asign to the variable
        itinerary_data = cur.fetchone()

        # Close the connection
        cur.close()

        # return the variable
        return itinerary_data

    # Update the day no in Itinerary
    def updateDayNo(self, day_no, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            UPDATE itinerary
            SET day_no = %s
            WHERE itinerary_id = %s
        ''', (day_no, itinerary_id))

        # Commite to the DB
        mysql.connection.commit()

        # Close the connection
        cur.close()
