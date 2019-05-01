# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql
from passlib.hash import sha256_crypt

class adminModel(object):

        # Admin Register
    def registerAdmin(self, admin_name, email, username, password):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO admin(name, email, username, password) VALUES(%s,%s,%s,%s)", (admin_name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Add Vendor Data
    def addVendorData(self, vendor_type):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO vendor(vendor_type) VALUES(%s)", (vendor_type,))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Fetch All Vendor Data
    def vendorFetchData(self):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("SELECT * FROM vendor")

        vendor_data = cur.fetchall()

        return vendor_data

    # Fetch One Vendor Data
    def vendorDataFetchOne(self, id):
        # fill the form from database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get article id
        cur.execute("SELECT * FROM vendor WHERE vendor_id = %s", [id])

        vendor_data = cur.fetchone()
        cur.close()

        return vendor_data

    # Edit Vendor Data
    def editVendorDAta(self, vendor_type, vendor_id):
        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("UPDATE vendor SET vendor_type=%s WHERE vendor_id=%s",(vendor_type, vendor_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()


    # Delete Vendor Data
    def deleteVendorData(self, vendor_id):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("DELETE FROM vendor WHERE vendor_id = %s", [vendor_id])

        # Commit to DB
        mysql.connection.commit()

        # Close
        cur.close()

    # Fetch the admin data
    def adminIdFetchOne(self, username):
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT admin_id FROM admin
            WHERE username = %s
        ''', [username])

        admin_data = cur.fetchone()

        return admin_data
