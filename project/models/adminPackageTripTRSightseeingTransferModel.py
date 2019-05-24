# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPackageTripTRSightseeingTransferModel(object):

    # Adding the Transaction for Sightseeing Transfer to Itinerary
    def addPackageTripSightseeingTransferData(self, sightseeing_transfer_id, package_trip_id, day_no, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT INTO tr_package_trip_sightseeing_transfer
            (sightseeing_transfer_id, package_trip_id, day_no, itinerary_id)
            VALUES (%s, %s, %s, %s)
        ''', (sightseeing_transfer_id, package_trip_id, day_no, itinerary_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Updating the Transaction for Sightseeing Transfer to Itinerary
    def updatePackageTripSightseeingTransferData(self, day_no, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            UPDATE tr_package_trip_sightseeing_transfer
            SET day_no = %s
            WHERE itinerary_id = %s
        ''', (day_no, itinerary_id))

        # Commite to the DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Deleting the Transaction for Sightseeing Transfer to Itinerary
    def deletePackageTripSightseeingTransferData(self, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            DELETE FROM  tr_package_trip_sightseeing_transfer WHERE itinerary_id = %s
        ''', [itinerary_id])

        # Commite to DB
        mysql.connection.commit()

        # Close the DB connection
        cur.close()
