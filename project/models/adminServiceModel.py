# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql
from passlib.hash import sha256_crypt

class adminServiceModel(object):

    # Add Service Data
    def addServiceData(self, name_of_service, trip_id, slug):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO service(name_of_service, trip_id, slug) VALUES(%s, %s, %s)", (name_of_service, trip_id, slug))

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Fetch Data
    def serviceFetchData(self, destination):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT `service`.`name_of_service`,`service`.`slug`, `service`.`service_id`, `trip`.`country`, `trip`.`destination`
            FROM `service`, `trip`
            WHERE `service`.`trip_id` = `trip`.`trip_id` AND
            `trip`.`destination` = %s
        ''', [destination])

        service_data = cur.fetchall()

        return service_data

    # Delete the Services
    def serviceDataDelete(self, service_id):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("DELETE FROM service WHERE service_id = %s", [service_id])

        # Commit to DB
        mysql.connection.commit()

        # Close
        cur.close()

    # Fetch Data from trip_id
    def serviceDataFetchOne(self, trip_id):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT * FROM service
            WHERE trip_id = %s
        ''', [trip_id])

        service_data = cur.fetchall()

        return service_data

        # close
        cur.close()
