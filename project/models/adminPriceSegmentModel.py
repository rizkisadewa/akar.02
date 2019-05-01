from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminPriceSegmentModel(object):

    # Add the Price Segment Data
    def addPriceSegmentData(self, segment_type, validity_date_start, validity_date_finish):
        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO price_segment(segment_type, validity_date_start, validity_date_finish) VALUES(%s, %s, %s)",
        (segment_type, validity_date_start, validity_date_finish))

        # commit to DB
        mysql.connection.commit()

        # close the connection
        cur.close()

    # Fetch Price Segment Data
    def priceSegmentFetchData(self):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("SELECT * FROM price_segment")

        # assign to the other variable that would be returned
        price_segment_data = cur.fetchall()

        return price_segment_data

    # Deleting the Price Segment Data
    def deletePriceSegmentData(self, price_segment_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("DELETE FROM price_segment WHERE price_segment_id = %s", [price_segment_id])

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Fetch One Data
    def priceSegmentFetchOne(self, price_segment_id):
        # fill the form from the database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get price_segment_id
        cur.execute("SELECT * FROM price_segment WHERE price_segment_id = %s", [price_segment_id])

        # asign the result to the variable
        price_segment_data = cur.fetchone()

        # close the connection
        cur.close()

        return price_segment_data

    # Updating the Price Segment
    def updatePriceSegment(self, segment_type, validity_date_start, validity_date_finish, price_segment_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("UPDATE price_segment SET segment_type=%s, validity_date_start=%s, validity_date_finish=%s WHERE price_segment_id = %s", (segment_type, validity_date_start, validity_date_finish, price_segment_id))

        # Commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()
