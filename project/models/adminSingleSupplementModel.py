# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql

class adminSingleSupplementModel(object):

    # Checking the Single Supplement
    def chkSingleSupplement(self, rate_card_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT COUNT(*) FROM single_supplement
            WHERE rate_card_id = %s
        ''', [rate_card_id])

        # Asign to the variable
        rate_card_checker = cur.fetchone()

        # close the connection
        cur.close()

        # return the variable
        return rate_card_checker

    # Add Single Supplement Data
    def addSingleSupplementData(self, price_segment_id, admin_id, min_pax, max_pax, price_per_person, rate_card_id):

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            INSERT INTO single_supplement(price_segment_id,admin_id, min_pax, max_pax, price_per_person, rate_card_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''',(price_segment_id, admin_id, min_pax, max_pax, price_per_person, rate_card_id))

        # Commit to DB
        mysql.connection.commit()

        # close the connection
        cur.close()

    # Fetch the Single Supplement Data
    def singleSupplementFetchData(self):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT `single_supplement`.*, `price_segment`.`validity_date_start`, `price_segment`.`validity_date_finish`
            FROM `single_supplement`, `price_segment`
            WHERE `single_supplement`.`price_segment_id` = `price_segment`.`price_segment_id`
            ORDER BY `single_supplement`.`min_pax` AND `price_segment`.`segment_type`
        ''')

        # Asign to the other variable that would be returned
        single_supplement_data = cur.fetchall()

        # Closing the Database
        cur.close()

        # Returning the variable
        return single_supplement_data
