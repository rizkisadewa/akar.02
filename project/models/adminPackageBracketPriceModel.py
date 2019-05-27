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
