# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPackageTripTRAirportTransferModel(object):

    # Adding the Transaction for Airport Transfer to Itinerary
    def addPackageTripAirportTransferData(self, airport_transfer_id, package_trip_id, day_no, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT INTO tr_package_trip_airport_transfer
            (airport_transfer_id, package_trip_id, day_no, itinerary_id)
            VALUES (%s, %s, %s, %s)
        ''', (airport_transfer_id, package_trip_id, day_no, itinerary_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Updateing the Transaction for Airport Transfer to Itinerary
    def updatePackageTripAirportTransferData(self, day_no, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            UPDATE tr_package_trip_airport_transfer
            SET day_no = %s
            WHERE itinerary_id = %s
        ''', (day_no, itinerary_id))

        # Commite to the DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Deleting the Transaction for Airport Transfer to Itinerary
    def deletePackageTripAirportTransferData(self, itinerary_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            DELETE FROM  tr_package_trip_airport_transfer WHERE itinerary_id = %s
        ''', [itinerary_id])

        # Commite to DB
        mysql.connection.commit()

        # Close the DB connection
        cur.close()
