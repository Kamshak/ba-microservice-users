# coding: utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = True
if os.environ['MYSQL_HOST']:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://' + os.environ['MYSQL_USER'] + ':' + os.environ['MYSQL_PASSWORD'] + '@' + os.environ['MYSQL_HOST'] + '/' + os.environ['MYSQL_DATABASE']
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'users.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
