# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class clientPackageTripModel(object):

    # Obtaining the trip_id from destination
    def tripIdFetchOne(self, destination):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `trip`.`trip_id`

            FROM
            `trip`

            WHERE
            `trip`.`destination` = %s
        ''', [destination])

        # Asign to the variable
        trip_id = cur.fetchone()

        # Close the connection
        cur.close()

        # return the variable
        return trip_id

    # Obtaining the data from index #booking form
    def packageTripOptionsFetchData(self, trip_id):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `package_trip`.`package_trip_name`,
            `package_trip`.`tag_line`,
            `package_trip_image`.`path`

            FROM
            `package_trip`,
            `service`,
            `trip`,
            `package_trip_image`

            WHERE
            `service`.`trip_id` = %s
            AND
            `package_trip`.`service_id` = `service`.`service_id`
            AND
            `package_trip`.`package_trip_image_profile` = `package_trip_image`.`package_trip_image_id`

        ''', [trip_id])

        # Asign to the variable
        package_trip_options_data = cur.fetchall()

        # close the connection
        cur.close()

        # return the variable
        return package_trip_options_data
