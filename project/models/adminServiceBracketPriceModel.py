# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminServiceBracketPriceModel(object):

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

    # Adding the data into Service Bracket Price
    def addServiceBracketPrice(self, min_pax, max_pax, price_per_person, service_id, price_segment_id):
        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO service_bracket_price(min_pax, max_pax, price_per_person, service_id, price_segment_id) VALUES(%s, %s, %s, %s, %s)",
        (min_pax, max_pax, price_per_person, service_id, price_segment_id))

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Fetch All The Data from Service Bracket Price
    def serviceBracketPriceFetchData(self, service_id):
        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
        SELECT `service_bracket_price`. *, `price_segment`.*
        FROM `service_bracket_price`, `price_segment`
        WHERE `service_bracket_price`.`service_id` = %s AND `service_bracket_price`.`price_segment_id` = `price_segment`.`price_segment_id`
        ORDER BY `service_bracket_price`.`min_pax`
        ''',[service_id])

        # assign to the other variable that would be returned
        service_bracket_price_data = cur.fetchall();

        # Close the connection
        cur.close()

        # return the variable
        return service_bracket_price_data

    # Delete the Service Bracket Price
    def deleteServiceBracketPrice(self, service_bracket_price_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('DELETE FROM service_bracket_price WHERE service_bracket_price_id = %s', [service_bracket_price_id])

        # commt the DB
        mysql.connection.commit()

        # Closing the Cursor
        cur.close()
