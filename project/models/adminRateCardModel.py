# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminRateCardModel(object):

    # Add the Rate Card Data
    def addRateCardData(self, package_trip_id, name_of_rate):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            INSERT IGNORE INTO rate_card(package_trip_id, name_of_rate) VALUES (%s, %s)
        ''',(package_trip_id, name_of_rate))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Counting the total of row
    def countingRateCardData(self, package_trip_id, name_of_rate):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT COUNT(*) FROM rate_card WHERE package_trip_id = %s AND name_of_rate = %s;
        ''', (package_trip_id, name_of_rate))

        # Asign to the variable
        checker = cur.fetchone()

        # Return the variable
        return checker

        # Close the connection
        cur.close()

    # Fetch the Rate Card
    def rateCardDataFetchAll(self, package_trip_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT * FROM rate_card WHERE package_trip_id = %s
        ''', [package_trip_id])

        # Asign to the variable
        rate_card_data = cur.fetchall()

        # Return the variable
        return rate_card_data

        # Close the connection
        cur.close()

    # Deleting the Rate Card
    def deleteRateCardData(self, rate_card_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            DELETE FROM rate_card WHERE rate_card_id = %s
        ''',[rate_card_id])

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
