# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPackageExcursionModel(object):

    # Fetch All service Data
    def packageExcursionFetchData(self):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            SELECT `package_excursion`.*, `trip`.`destination`, `trip`.`country`,`trip`.`trip_id`
            FROM `package_excursion`, `trip`
            WHERE `package_excursion`.`trip_id` = `trip`.`trip_id`
            ORDER BY `package_excursion`.`package_excursion_id`
        ''')

        services_data = cur.fetchall()

        return services_data


    # Add the Package Excursion Data
    def addPackageExcursionData(self, package_title, package_description, inclusions, estimation_time_start, estimation_time_finish, trip_id):
        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO package_excursion(package_title, package_description, inclusions, estimation_time_start, estimation_time_finish, trip_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (package_title, package_description, inclusions, estimation_time_start, estimation_time_finish, trip_id))

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Delete the Package Excursion Data
    def deletePackageExcursionData(self, package_excursion_id):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("DELETE FROM package_excursion WHERE package_excursion_id = %s", [package_excursion_id])

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Fetch One data
    def packageExcursionDataFetchOne(self, package_excursion_id):
        # fill the form from database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get package excursion
        cur.execute("SELECT * FROM package_excursion WHERE package_excursion_id = %s", [package_excursion_id])

        package_excursion_data = cur.fetchone()
        cur.close()

        return package_excursion_data

    # Update Package Excursion Data
    def updatePackageExcursionData(self, package_title, package_description, inclusions, estimation_time_start, estimation_time_finish, trip_id, package_excursion_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("UPDATE package_excursion SET package_title=%s, package_description=%s, inclusions=%s, estimation_time_start=%s, estimation_time_finish=%s, trip_id=%s WHERE package_excursion_id=%s",
        (package_title, package_description, inclusions, estimation_time_start, estimation_time_finish, trip_id, package_excursion_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Fetch the data which is refer to the tripID
    def packageExcrusionDataFetchFromTripId(self, trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute the query
        cur.execute('''
            SELECT * FROM package_excursion
            WHERE trip_id = %s
        ''', [trip_id])

        # Asign to the data
        package_excursion_data = cur.fetchall()

        # Close the DB
        cur.close()

        return package_excursion_data
