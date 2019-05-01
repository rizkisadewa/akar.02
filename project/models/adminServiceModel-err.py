# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql
from passlib.hash import sha256_crypt

class adminServiceModel-err(object):

    # Fetch Service Trip Data
    def serviceTripFetchData(self, destination_data):
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute the query
        cur.execute('''
            SELECT destination, country, trip_id FROM trip
            WHERE destination = %s
        ''', [destination_data])

        service_trip_data = cur.fetchone()

        # close the DB
        cur.close()

        # return the variable
        return service_trip_data

    # Fetch One of Trip id
    def tripIdFetchOne(self, destination):
        # fill the form from database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get package excursion id
        cur.execute("SELECT trip_id FROM trip WHERE destination = %s", [destination])

        trip_id = cur.fetchone()
        cur.close()

        return trip_id


    # Add Service Data
    def addServiceData(self, name_of_service, trip_id, validity_date_start, validity_date_finish, tag_line, inclusions):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO services(name_of_service, trip_id, validity_date_start, validity_date_finish, tag_line, inclusions) VALUES(%s, %s, %s, %s, %s, %s)", (name_of_service, trip_id, validity_date_start, validity_date_finish, tag_line, inclusions))

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Fetch All service Data
    def serviceFetchData(self, trip_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            SELECT * FROM services
            WHERE trip_id = %s
        ''', [trip_id])

        service_data = cur.fetchall()

        # Close the connection to DB
        cur.close()

        return service_data

    # Delete Service Data
    def deleteServiceData(self, service_id):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("DELETE FROM services WHERE service_id = %s", [service_id])

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Fetch One data
    def serviceDataFetchOne(self, service_id):
        # fill the form from database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get service id
        cur.execute("SELECT * FROM services WHERE service_id = %s", [service_id])

        service_data = cur.fetchone()
        cur.close()

        return service_data

    # Update Service Data
    def updateServiceData(self, name_of_service, trip_id, validity_date_start, validity_date_finish, tag_line, inclusions, service_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("UPDATE services SET name_of_service=%s, trip_id=%s, validity_date_start=%s, validity_date_finish=%s, tag_line=%s, inclusions=%s WHERE service_id=%s", (name_of_service, trip_id, validity_date_start, validity_date_finish, tag_line, inclusions, service_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # ** CHECKING FILE TOTAL ROW **
    # service_detail
    def serviceDetailTotal(service_id):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('SELECT SUM( service_id =%s ) FROM service_detail', [service_id])

        service_detail_data = cur.fetchone()

        return service_detail_data


    # service_image
    def serviceImageTotal(service_id):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('SELECT SUM( service_id =%s ) FROM service_image', [service_id])

        service_image_data = cur.fetchone()

        return service_image_data

    # set the service image id to null
    def setServiceImageIdNull(self, service_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('UPDATE services SET service_image_id = NULL, file_name = NULL WHERE service_id=%s', [service_id])

        # commit to the DB
        mysql.connection.commit()

        # Close the connection
        cur.close()
