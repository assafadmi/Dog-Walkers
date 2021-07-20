# -------------------------------------------------------------------------------
# walkrequest 
# -------------------------------------------------------------------------------
# A class to manage the walkerrequests -create and save in the DB
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------

#import users to find email 
from google.appengine.api import users
#import db handler to interact with DB
import db_handler

class WalkRequest():
    def __init__(self):
        self.DbHandler=db_handler.DbHandler()
        # create data members
        self.number = ""
        self.walk_request_date = ""
        self.day = ""
        self.part_of_the_day = ""
        self.cancellation_date = ""
        self.respond_date = ""
        self.status = 'waiting'
        self.dog_id = ""
        self.walker_email = ""
    
    # a function to insert walk request to DB
    def insertToDb(self):
		self.DbHandler.connectToDb()
		cursor=self.DbHandler.getCursor()
		sql = 	"""
				INSERT INTO walk_requests(walk_request_date,day,part_of_the_day,status,dog_id,walker_email)
				VALUES(sysdate(),%s,%s,%s,%s,%s)
				"""
		cursor.execute(sql,(self.day, self.part_of_the_day,self.status,self.dog_id,self.walker_email))
		self.DbHandler.commit()
		self.DbHandler.disconnectFromDb()
		return
    

    # a function to update walk request status (confirmed, waiting, declined)
    def update_status(self,email,status):
        self.DbHandler.connectToDb()
        cursor=self.DbHandler.getCursor()
        sql_1 = """
            UPDATE walk_requests
            SET status = %s 
            WHERE walker_email = %s
            """
        cursor.execute(sql_1, (status, email))
        sql_2 = """
            UPDATE walk_requests
            SET respond_date = sysdate()
            WHERE walker_email = %s
            """
        cursor.execute(sql_2,(email))
        self.DbHandler.commit()
        self.DbHandler.disconnectFromDb()
        return
    