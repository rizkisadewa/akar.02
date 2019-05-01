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
