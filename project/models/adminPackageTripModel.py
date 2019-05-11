# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPackageTripModel(object):

    # Add Package Trip Data
    def addPackageTrip(self, service_id, admin_id, package_trip_name, validity_date_start, validity_date_finish, tag_line, inclusions):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO package_trip(service_id, admin_id, package_trip_name, validity_date_start, validity_date_finish, tag_line, inclusions) VALUES(%s, %s, %s, %s, %s, %s, %s)",
        (service_id, admin_id, package_trip_name, validity_date_start, validity_date_finish, tag_line, inclusions))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()


    # Fetch The Package Trip Data
    def packageTripFetchData(self, trip_id, destination):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `package_trip`.`package_trip_id`,
            `package_trip`.`package_trip_name`,
            `service`.`service_id`,
            `trip`.`destination`,
            `trip`.`country`,
            `admin`.`name`
            FROM `package_trip`, `trip`, `admin`, `service`
            WHERE `package_trip`.`service_id` = `service`.`service_id` AND
            `service`.`trip_id` = %s AND `admin`.`admin_id` = `package_trip`.`admin_id`
            AND `trip`.`destination` = %s
        ''', (trip_id, destination))

        # Asign to the variable
        package_trip_data = cur.fetchall()

        # Close the connection
        cur.close()

        # return the variable
        return package_trip_data

    # Fetch One Package Trip Data
    def packageTripDataFetchOne(self, package_trip_id):

        # fill the form from database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get Package Trip Data from query
        cur.execute("SELECT * FROM package_trip WHERE package_trip_id = %s", [package_trip_id])

        # Asign to the Variable
        package_trip_fetch_one_data = cur.fetchone()

        # Close the connection
        cur.close()

        return package_trip_fetch_one_data

    # Update the Package Trip Data
    def updatePackageTripData(self, package_trip_name, tag_line, validity_date_start, validity_date_finish, inclusions, package_trip_id):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            UPDATE package_trip
            SET
            package_trip_name = %s,
            tag_line = %s,
            validity_date_start = %s,
            validity_date_finish = %s,
            inclusions = %s
            WHERE
            package_trip_id = %s
        ''', (package_trip_name, tag_line, validity_date_start, validity_date_finish, inclusions, package_trip_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Delete the Package Trip Data
    def deletePackageTripData(self, package_trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("DELETE FROM package_trip WHERE package_trip_id = %s", [package_trip_id])

        # Commit to DB
        mysql.connection.commit()

        # Close
        cur.close()

    # Add the Package Trip Component
    def addPackageTripComponent(self, day_excursion_id, package_trip_id, day_no):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO tr_package_trip_day_excursion(day_excursion_id, package_trip_id, day_no) VALUES(%s, %s, %s)",
        (day_excursion_id, package_trip_id, day_no))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Package Trip Component Data
    def packageTripComponentData(self, package_trip_id, package_trip_id_2):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `tr_package_trip_day_excursion`.`day_no`,
            `tr_package_trip_day_excursion`.`tr_package_trip_day_excursion_id`,
            `package_trip`.`package_trip_name`
            FROM `tr_package_trip_day_excursion`, `package_trip`
            WHERE `package_trip`.`package_trip_id` = %s
            AND `tr_package_trip_day_excursion`.`package_trip_id` = %s
        ''', (package_trip_id, package_trip_id_2))

        # Asign to the variable
        component_data = cur.fetchall()

        # Close the connection
        cur.close()

        # return the variable
        return component_data

    # Package Trip Component Data Fetch One
    def packageTripComponentDataFetchOne(self, package_trip_id, tr_package_trip_day_excursion_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `tr_package_trip_day_excursion`.`day_no`,
            `tr_package_trip_day_excursion`.`tr_package_trip_day_excursion_id`,
            `package_trip`.`package_trip_name`
            FROM `tr_package_trip_day_excursion`, `package_trip`
            WHERE `package_trip`.`package_trip_id` = %s
            AND `tr_package_trip_day_excursion`.`tr_package_trip_day_excursion_id` = %s
        ''', (package_trip_id, tr_package_trip_day_excursion_id))

        # Asign to the variable
        component_data = cur.fetchone()

        # Close the connection
        cur.close()

        # return the variable
        return component_data

    # Package Trip component Update Day No
    def packageTripComponentUpdateData(self, day_no, tr_package_trip_day_excursion_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            UPDATE tr_package_trip_day_excursion
            SET
            day_no = %s
            WHERE
            tr_package_trip_day_excursion_id = %s
        ''', (day_no, tr_package_trip_day_excursion_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
