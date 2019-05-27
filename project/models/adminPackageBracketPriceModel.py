# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPackageBracketPriceModel(object):

    # Checking the Price Bracket Price
    def chkPriceBracketPrice(self, rate_card_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT COUNT(*) FROM package_bracket_price
            WHERE rate_card_id = %s
        ''', [rate_card_id])

        # Asign to the variable
        rate_card_checker = cur.fetchone()

        # close the connection
        cur.close()

        # return the variable
        return rate_card_checker

    # Add Package Bracket Price Data
    def addPackageBracketPriceData(self, price_segment_id, admin_id, min_pax, max_pax, price_per_person, rate_card_id):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            INSERT INTO package_bracket_price(price_segment_id,admin_id, min_pax, max_pax, price_per_person, rate_card_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''',(price_segment_id, admin_id, min_pax, max_pax, price_per_person, rate_card_id))

        # Commit to DB
        mysql.connection.commit()

        # close the connection
        cur.close()

    # Fetch the Package Bracket Price
    def packageBracketPriceDataFetchData(self):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT `package_bracket_price`.*, `price_segment`.`validity_date_start`, `price_segment`.`validity_date_finish`
            FROM `package_bracket_price`, `price_segment`
            WHERE `package_bracket_price`.`price_segment_id` = `price_segment`.`price_segment_id`
            ORDER BY `package_bracket_price`.`min_pax` AND `price_segment`.`segment_type`
        ''')

        # Asign to the other variable that would be returned
        package_bracket_price_data = cur.fetchall()

        # Closing the Database
        cur.close()

        # Returning the variable
        return package_bracket_price_data

    # Deleting the Package Bracket Price
    def deletePackageBracketPrice(self, package_bracket_price_id):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('DELETE FROM package_bracket_price WHERE package_bracket_price_id = %s', [package_bracket_price_id])

        # commit to the DB
        mysql.connection.commit()

        # Close the cursor
        cur.close()
