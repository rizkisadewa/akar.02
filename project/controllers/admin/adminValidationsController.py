# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from project import mysql
from passlib.hash import sha256_crypt
from functools import wraps

class adminValidation(object):

    def adminLogin(self, username, password_candidate):
        # Create cursor
        cur = mysql.connection.cursor()

        #Get user by Username
        result = cur.execute("SELECT * FROM admin WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Password, if correct will return true
            if sha256_crypt.verify(password_candidate, password):
                return True

            else:
                error = 'Password is not correct'
                flash('Password is not correct', 'danger')
                return render_template('admin/adminLogin.html', error=error)
                # close the connection
                cur.close()
        else:
            error = 'Username not found'
            flash('Username not found', 'danger')
            return render_template('admin/adminLogin.html', error=error)

    # Admin Logout is only use for
    def adminLogout(self):
        session.clear() #clear the session
        flash('You are now logged out', 'success')
        return redirect(url_for('adminLogin'))
