# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPackageTripTRAirportTransferModel(object):

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
