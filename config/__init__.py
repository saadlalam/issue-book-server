#!/usr/bin/env python
import pymysql
import pymysql.cursors
import logging

ENV = "dev"
usersPath = 'users'
issuesPath = 'issues'
SERVICE_ACCOUNT_FILE = 'config/key.json'
AUTHORIZED_ORIGIN = '*'
DEBUG = True

"""
This file contains all of the configuration values for the application.
Update this file with the values for your specific Google Cloud project.
You can create and manage projects at https://console.developers.google.com
"""
# To be changed for acceptance and production
