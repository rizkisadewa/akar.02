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
    def dayExcursionFetchData(self, trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            `day_excursion`.`day_excursion_id`,
            `day_excursion`.`day_excursion_title`,
            `admin`.`name`
            FROM `day_excursion`, `admin`, `service`
            WHERE `day_excursion`.`admin_id` = `admin`.`admin_id` AND `day_excursion`.`service_id` = `service`.`service_id`
            AND `service`.`trip_id` = %s
        ''', [trip_id])

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


    # Update the Day Excursions Data
    def updateDayExcursionData(self, day_excursion_title, inclusions, estimation_time_start, estimation_time_finish, day_excursions_description, day_excursion_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            UPDATE day_excursion
            SET
            day_excursion_title = %s,
            inclusions = %s,
            estimation_time_start = %s,
            estimation_time_finish = %s,
            day_excursions_description = %s
            WHERE
            day_excursion_id = %s
        ''', (day_excursion_title, inclusions, estimation_time_start, estimation_time_finish, day_excursions_description, day_excursion_id))

        # Commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Delete the Day Excusion Data
    def deleteDayExcursionData(self, day_excursion_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            DELETE FROM day_excursion WHERE day_excursion_id = %s
        ''', [day_excursion_id])

        # Commit to DB
        mysql.connection.commit()

        # close the DB
        cur.close()

    # Fetch the Day Excursion refer to service id
    def dayExcursionDataFetchOneServiceId(self, service_id):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            day_excursion_id, day_excursion_title
            FROM day_excursion
            WHERE service_id = %s
        ''', [service_id])

        # Asign to the variable
        day_excursion_data = cur.fetchall()

        # Close the connection
        cur.close()

        # return the variable
        return day_excursion_data


    # Fetch the Day Excursion refer to service id
    def dayExcursionIdFetchOneServiceId(self, service_id):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT
            day_excursion_id
            FROM day_excursion
            WHERE service_id = %s
        ''', [service_id])

        # Asign to the variable
        day_excursion_id = cur.fetchall()

        # Close the connection
        cur.close()

        # return the variable
        return day_excursion_id
