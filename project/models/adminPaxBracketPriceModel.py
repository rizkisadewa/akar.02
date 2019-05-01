# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPaxBracketPriceModel(object):

    # Fetch Price Segment ID refer to segment_type that input in the form
    def priceSegmentIdFetchOne(self, segment_type):
        # fill the form from databased
        # create a cursor
        cur = mysql.connection.cursor()

        # Get price segment id
        cur.execute("SELECT price_segment_id FROM price_segment WHERE segment_type = %s", [segment_type])

        # obtain the price segment type id
        price_segment_id = cur.fetchone()
        cur.close()

        return price_segment_id

    # Adding the data into Pax Bracket Price
    def addPaxBracketPrice(self, min_pax, max_pax, price_per_person, price_segment_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO pax_bracket_price(min_pax, max_pax, price_per_person, price_segment_id) VALUES (%s, %s, %s, %s)",
        (min_pax, max_pax, price_per_person, price_segment_id))

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Fetch Pax Bracket Price Data
    def paxBracketPriceFetchData(self):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
        SELECT `pax_bracket_price`.*, `price_segment`.*
        FROM `price_segment`, `pax_bracket_price`
        WHERE `pax_bracket_price`.`price_segment_id` = `price_segment`.`price_segment_id`
        ORDER BY `price_segment`.`segment_type` AND `pax_bracket_price`.`min_pax`
        ''')

        # assign to the other variable that would be returned
        pax_bracket_price_data = cur.fetchall();

        # Close the connection
        cur.close()

        # return the variable
        return pax_bracket_price_data

    # Delete the Pax Bracket Price Data
    def deletePaxBracketPrice(self, pax_bracket_price_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('DELETE FROM pax_bracket_price WHERE pax_bracket_price_id = %s', [pax_bracket_price_id])

        # commit to DB
        mysql.connection.commit()

        # Closing the Cursor
        cur.close()
