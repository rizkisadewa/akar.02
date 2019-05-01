# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask, send_from_directory, request
from flask_mysqldb import MySQL

# from flask_debugtoolbar import DebugToolbarExtension
app = Flask('project', static_folder='static')

app.config['SECRET_KEY'] = 'random'
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myakar01'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configuration in Deployment

# app.config['SECRET_KEY'] = 'random'
# # Config MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'jepunkuc'
# app.config['MYSQL_PASSWORD'] = 'ird26y4B2E'
# app.config['MYSQL_DB'] = 'jepunkuc_myakar-v0.3'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

app.debug = True
# toolbar = DebugToolbarExtension(app)
from project.controllers import *
from project.controllers.client import *
from project.controllers.admin import *


# Robots
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
