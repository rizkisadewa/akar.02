# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPackageTripTRDayExcursionModel(object):

    # Adding the Transaction for Day Excursion to Itinerary
    def addPackageTripDayExcursionData(self, day_excursion_id, package_trip_id, day_no, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT INTO tr_package_trip_day_excursion
            (day_excursion_id, package_trip_id, day_no, itinerary_id)
            VALUES (%s, %s, %s, %s)
        ''', (day_excursion_id, package_trip_id, day_no, itinerary_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Updating the Transaction for Day Excursion to Itinerary
    def updatePackageTripDayExcursionData(self, day_no, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            UPDATE tr_package_trip_day_excursion
            SET day_no = %s
            WHERE itinerary_id = %s
        ''', (day_no, itinerary_id))

        # Commite to the DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Deleting the Transaction for Day Excursion to Itinerary
    def deletePackageTripDayExcursionData(self, itinerary_id):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            DELETE FROM  tr_package_trip_day_excursion WHERE itinerary_id = %s
        ''', [itinerary_id])

        # Commite to DB
        mysql.connection.commit()

        # Close the DB connection
        cur.close()
