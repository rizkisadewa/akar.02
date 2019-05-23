# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminSightseeingTransferModel(object):

    # Add Sightseeing Transfer Data
    def addSightseeingTransferData(self, service_id, admin_id, sightseeing_transfer_title, inclusions, pickup_point, drop_off_point, duration, sightseeing_transfer_description):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT INTO sightseeing_transfer(service_id, admin_id, sightseeing_transfer_title, inclusions, pickup_point, drop_off_point, duration, sightseeing_transfer_description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (service_id, admin_id, sightseeing_transfer_title, inclusions, pickup_point, drop_off_point, duration, sightseeing_transfer_description))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Fetch the Data Refer to the Trip Data
    def sightseeingTransferFetchData(self, trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `sightseeing_transfer`.`sightseeing_transfer_id`,
            `sightseeing_transfer`.`sightseeing_transfer_title`,
            `admin`.`name`
            FROM `sightseeing_transfer`, `admin`, `service`
            WHERE `sightseeing_transfer`.`admin_id` = `admin`.`admin_id`
            AND `sightseeing_transfer`.`service_id` = `service`.`service_id`
            AND `service`.`trip_id` = %s
        ''', [trip_id])

        # Asign to the variable
        sightseeing_transfer_data = cur.fetchall()

        # Close the connection
        cur.close()

        # return the variable
        return sightseeing_transfer_data
