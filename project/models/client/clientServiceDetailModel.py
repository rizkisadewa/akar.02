# -*- coding: utf-8 -*-
from flask import Flask
from project import mysql

class clientServiceDetailModel(object):

    # Fetch One the Destination Data Refer to the Service id
    def destinationSrvDtlFetchOneData(self, service_id):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT * FROM services
            WHERE service_id = %s
        ''', [service_id])

        # asign to the variable
        destination_srv_dtl_data = cur.fetchone()

        # close the connection
        cur.close()

        return destination_srv_dtl_data

    # Fetch Data the Service Image Refer to the Service id
    def serviceImageDataFetchData(self, service_id):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT file_name FROM service_image
            WHERE service_id = %s
        ''', [service_id])

        # asign to the variable
        service_image_data = cur.fetchall()

        # close the connection
        cur.close()

        return service_image_data

    # Fetch the Program Detail, combining 2 Table : Service Detail and Package Excursions
    def programDetailFetchOne(self, service_id):

        # Create a Cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute('''
            SELECT `service_detail`.`day_no`, `package_excursion`.`package_title`, `package_excursion`.`package_description`
            FROM  `service_detail`,  `package_excursion`
            WHERE `service_detail`.`package_excursion_id` = `package_excursion`.`package_excursion_id`
            AND `service_detail`.`service_id` = %s
            ORDER BY `day_no`
        ''', [service_id])

        # asign to the variable
        program_detail_data = cur.fetchall()

        # close the connection
        cur.close()

        return program_detail_data
