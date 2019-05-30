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
            `service`.`name_of_service`,
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
    def updatePackageTripData(self, package_trip_name, tag_line, validity_date_start, validity_date_finish, inclusions, service_id, package_trip_id):
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
            inclusions = %s,
            service_id = %s
            WHERE
            package_trip_id = %s
        ''', (package_trip_name, tag_line, validity_date_start, validity_date_finish, inclusions, service_id, package_trip_id))

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


    # Package Trip Component Data
    def packageTripComponentData(self, package_trip_id, package_trip_id_2, package_trip_id_3, package_trip_id_4):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `itinerary`.`day_no`,
            `tr_package_trip_day_excursion`.`tr_package_trip_day_excursion_id`,
            `day_excursion`.`day_excursion_title`,
            `package_trip`.`package_trip_name`,
            `tr_package_trip_airport_transfer`.`day_no`

            FROM
            `tr_package_trip_day_excursion`,
            `package_trip`,
            `day_excursion`,
            `tr_package_trip_airport_transfer`

            WHERE
            `package_trip`.`package_trip_id` = %s
            AND `tr_package_trip_day_excursion`.`package_trip_id` = %s
            AND `tr_package_trip_day_excursion`.`day_excursion_id` = `day_excursion`.`day_excursion_id`
            AND `tr_package_trip_airport_transfer`.`package_trip_id` = %s
            AND `tr_package_trip_airport_transfer`.`airport_transfer_id` = %s

            ORDER BY
            `tr_package_trip_day_excursion`.`day_no`
            AND `tr_package_trip_airport_transfer`.`day_no`
        ''', (package_trip_id, package_trip_id_2, package_trip_id_3, package_trip_id_4))

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
            `day_excursion`.`day_excursion_title`,
            `tr_package_trip_airport_transfer`.`day_no`
            FROM
            `tr_package_trip_day_excursion`,
            `package_trip`,
            `day_excursion`,
            `airport_transfer`
            WHERE
            `package_trip`.`package_trip_id` = %s
            AND `tr_package_trip_day_excursion`.`tr_package_trip_day_excursion_id` = %s
            AND `tr_package_trip_day_excursion`.`day_excursion_id` = `day_excursion`.`day_excursion_id`
        ''', (package_trip_id, tr_package_trip_day_excursion_id))

        # Asign to the variable
        component_data = cur.fetchone()

        # Close the connection
        cur.close()

        # return the variable
        return component_data

    # Package Trip Image
    def addPackageTripImageData(self, path):

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO package_trip_image(path) VALUES (%s)",
        [path])

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Last Package Trip Image Id trigerred
    def lastPackageTripImageId(self):

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            SELECT MAX(package_trip_image_id) FROM package_trip_image
        ''')

        # Asign to the variable
        last_srv_img_id = cur.fetchone()

        return last_srv_img_id

    # Updating the Package Trip Image Data
    def editPackageTripImageData(self, package_trip_id, file_name, db_path, last_srv_img_id):


        # Create cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("UPDATE package_trip_image SET package_trip_id=%s, file_name=%s, path=%s WHERE package_trip_image_id=%s ",(package_trip_id, file_name, db_path, last_srv_img_id))

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Fetch the Package Trip Image Data
    def packageTripImageDataFetch(self, package_trip_id):

        # Create Crsor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("SELECT * FROM package_trip_image WHERE package_trip_id=%s", [package_trip_id])

        # asigning to the variable
        package_trip_image_data = cur.fetchall()

        return package_trip_image_data

    # set the Package Trip Image id to null
    def setPackageTripImageProfileNull(self, package_trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('UPDATE package_trip SET package_trip_image_profile = NULL, file_name = NULL WHERE package_trip_id=%s', [package_trip_id])

        # commit to the DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Delete Package Trip Image Data
    def deletePackageTripImage(self, package_trip_image_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("DELETE FROM package_trip_image WHERE package_trip_image_id = %s", [package_trip_image_id])

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Setting Package Trip Image Profile
    def setPackageTripImageProfile(self, package_trip_image_id, package_trip_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("UPDATE package_trip SET package_trip_image_profile =%s WHERE package_trip_id = %s", (package_trip_image_id, package_trip_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Fetch the Package Trip Image Profile
    def packageTripImageProfile(self, package_trip_image_profile):

        # fill the form from database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get Package Trip Data from query
        cur.execute("SELECT file_name FROM package_trip_image WHERE package_trip_image_id = %s", [package_trip_image_profile])

        # Asign to the Variable
        package_trip_image_profile = cur.fetchone()

        # Close the connection
        cur.close()

        return package_trip_image_profile
