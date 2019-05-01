# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from project import mysql
from passlib.hash import sha256_crypt

class adminServiceDetailModel(object):

    # Fetch Package Excrusion ID refer to package_title that input in the form
    def packageExcursionIdFetchOne(self, package_title):
        # fill the form from database
        # Create a Cursor
        cur = mysql.connection.cursor()

        # Get package excursion id
        cur.execute("SELECT package_excursion_id FROM package_excursion WHERE package_title = %s", [package_title])

        package_excursion_id = cur.fetchone()
        cur.close()

        return package_excursion_id

    # Fetch The Data
    def serviceDetailFetchData(self, service_id):
        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("SELECT * FROM service_detail WHERE service_id=%s ORDER BY day_no", [service_id])

        service_detail_data = cur.fetchall()

        return service_detail_data

    # Adding the data into Service Detail
    def addServiceDetailData(self, day_no, package_excursion_id, package_title, service_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO service_detail(day_no, package_excursion_id, package_title, service_id) VALUES (%s, %s, %s, %s)",
        (day_no, package_excursion_id, package_title, service_id))

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Deleting the component Service Details
    def deleteServiceDetailData(self, service_detail_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("DELETE FROM service_detail WHERE service_detail_id = %s", [service_detail_id])

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Adding the Image Service Data
    def addServiceImageData(self, path):

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT INTO service_image(path) VALUES (%s)",
        [path])

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Update the Image Service Data
    def editServiceImageData(self, service_id, file_name, db_path, last_srv_img_id):

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("UPDATE service_image SET service_id=%s, file_name=%s, path=%s WHERE service_image_id=%s ",(service_id, file_name, db_path, last_srv_img_id))

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()


    # Fetch the Service Image Data
    def serviceImageDataFetch(self, service_id):

        # Create Crsor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("SELECT * FROM service_image WHERE service_id=%s", [service_id])

        # asigning to the variable
        service_image_data = cur.fetchall()

        return service_image_data

    # Delete the Servimce Image Data
    def deleteServiceImageData(self, service_image_id):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("DELETE FROM service_image WHERE service_image_id = %s", [service_image_id])

        # commit to DB
        mysql.connection.commit()

        # Close the connection
        cur.close()

    # Set as Service Image Profile
    def setServiceImageProfile(self, service_image_id, service_id, file_name):

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("UPDATE services SET service_image_id=%s, file_name=%s WHERE service_id=%s", (service_image_id, file_name, service_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

    # Fetch Service Image Profile
    def serviceImageProfileDataFetch(self, file_name):

        # Create Crsor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            SELECT file_name FROM service_image
            WHERE file_name = %s
        ''', [file_name])

        # asigning to the variable
        service_image_data = cur.fetchall()

        return service_image_data

    # Fetch Last Service Image id
    def lastServiceImageId(self):

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute('''
            SELECT MAX(service_image_id) FROM service_image
        ''')

        # Asign to the variable
        last_srv_img_id = cur.fetchone()

        return last_srv_img_id
