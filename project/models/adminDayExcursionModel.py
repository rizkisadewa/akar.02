# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminDayExcursionModel(object):

    # Add Day Excursion Data
    def addDayExcursionData(self, service_id, admin_id, day_excursion_title, day_excursions_description, inclusions, estimation_time_start, estimation_time_finish):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT INTO day_excursion(service_id, admin_id, day_excursion_title, day_excursions_description, inclusions, estimation_time_start, estimation_time_finish)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (service_id, admin_id, day_excursion_title, day_excursions_description, inclusions, estimation_time_start, estimation_time_finish))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Fetch Day Excursion Data
    def dayExcursionFetchData(self):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `day_excursion`.`day_excursion_id`,
            `day_excursion`.`day_excursion_title`,
            `admin`.`name`
            FROM `day_excursion`, `admin`
            WHERE `day_excursion`.`admin_id` = `admin`.`admin_id`
        ''')

        # Asign to the variable
        day_excursion_data = cur.fetchall()

        # Close the connection
        cur.close()

        # return the variable
        return day_excursion_data

    # Fetch One Day Excursion Data
    def dayExcursionDataFetchOne(self, day_excursion_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute the query
        cur.execute("SELECT * FROM day_excursion WHERE day_excursion_id = %s", [day_excursion_id])

        # Asign to the Variable
        day_excursion_data = cur.fetchone()

        # Close the connection
        cur.close()

        return day_excursion_data
