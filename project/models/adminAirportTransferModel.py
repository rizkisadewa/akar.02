# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminAirportTransferModel(object):

    # Add Airport Transfer Data
    def addAirportTransferData(self, service_id, admin_id, airport_transfer_title, inclusions, pickup_point, drop_off_point, duration, airport_transfer_description):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT INTO airport_transfer(service_id, admin_id, airport_transfer_title, inclusions, pickup_point, drop_off_point, duration, airport_transfer_description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (service_id, admin_id, airport_transfer_title, inclusions, pickup_point, drop_off_point, duration, airport_transfer_description))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Fetch the Data Refer to the Trip Data
    def airportTransferFetchData(self, trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `airport_transfer`.`airport_transfer_id`,
            `airport_transfer`.`airport_transfer_title`,
            `admin`.`name`
            FROM `airport_transfer`, `admin`, `service`
            WHERE `airport_transfer`.`admin_id` = `admin`.`admin_id` AND `airport_transfer`.`service_id` = `service`.`service_id`
            AND `service`.`trip_id` = %s
        ''', [trip_id])

        # Asign to the variable
        airport_transfer_data = cur.fetchall()

        # Close the connection
        cur.close()

        # return the variable
        return airport_transfer_data

    # Fetch One the Data of Airport Transfer
    def airportTransferDataFetchOne(self, airport_transfer_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute the query
        cur.execute("SELECT * FROM airport_transfer WHERE airport_transfer_id = %s", [airport_transfer_id])

        # Asign to the Variable
        airport_transfer_data = cur.fetchone()

        # Close the connection
        cur.close()

        return airport_transfer_data

    # Updating the Airport Transfer Data
    def updateAirportTransferData(self, airport_transfer_title, inclusions, pickup_point, drop_off_point, duration, airport_transfer_description, airport_transfer_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            UPDATE airport_transfer
            SET
            airport_transfer_title = %s,
            inclusions = %s,
            pickup_point = %s,
            drop_off_point = %s,
            duration = %s,
            airport_transfer_description = %s
            WHERE
            airport_transfer_id = %s
        ''', (airport_transfer_title, inclusions, pickup_point, drop_off_point, duration, airport_transfer_description, airport_transfer_id))

        # Commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()
