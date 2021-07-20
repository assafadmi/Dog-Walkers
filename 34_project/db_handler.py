#-------------------------------------------------------------------------------
# db handler
# -------------------------------------------------------------------------------
# Class which connects the database with the app
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------
# import logging so we can write messages to the log
import logging
import os
#import DB library
import MySQLdb

# Database connection parameters 
DB_USER_NAME='db_team34'
DB_PASSWORD='wekjltwa'
DB_DEFALUT_DB='db_team34'

class DbHandler():
    def __init__(self):
        logging.info('Initializing DbHandler new')
        self.m_user=DB_USER_NAME
        self.m_password=DB_PASSWORD
        self.m_default_db=DB_DEFALUT_DB
        self.m_charset='utf8'
        self.m_host='34.122.221.36'
        self.m_port=3306
        self.m_DbConnection=None

    def connectToDb(self):
        logging.info('In ConnectToDb')
        # we will connect to the DB only once
        if self.m_DbConnection is None:
            # connect to the DB
            self.m_DbConnection = MySQLdb.connect(
            host=self.m_host,
            db=self.m_default_db,
            port=self.m_port,
            user= self.m_user,
            passwd=self.m_password,
            charset=self.m_charset)

    def disconnectFromDb(self):
        logging.info('In DisconnectFromDb')
        if self.m_DbConnection:
            self.m_DbConnection.close()
            
    def commit(self):
        logging.info('In commit')
        if self.m_DbConnection:
            self.m_DbConnection.commit()
            
    def getCursor(self):
        logging.info('In DbHandler.getCursor')
        self.connectToDb()
        return (self.m_DbConnection.cursor())