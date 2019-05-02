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
    def packageTripFetchData(self):
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
            `service`.`trip_id` = `trip`.`trip_id` AND `admin`.`admin_id` = `package_trip`.`admin_id`
        ''')

        # Asign to the variable
        package_trip_data = cur.fetchall()

        # return the variable
        return package_trip_data
