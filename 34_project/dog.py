#-------------------------------------------------------------------------------
# dog
# -------------------------------------------------------------------------------
# A class to manage dogs- create and insert to DB
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------

# import users to use its function
from google.appengine.api import users
# import dbhandler to interact with DB
import db_handler


class Dog():
    def __init__(self):
        self.d_DbHandler=db_handler.DbHandler()
        # create data members of the class 
        self.d_id = ""
        self.d_sex = ""
        self.d_name = ""
        self.d_age = ""
        self.d_size = ""
        self.d_friendly = ""
        self.d_immunized = ""
        self.d_owner_email = ""

    # function to insert dog into database
    def insertToDb(self):
		self.d_DbHandler.connectToDb()
		cursor=self.d_DbHandler.getCursor()
		sql = 	"""
				INSERT INTO dogs(id,sex,name,age,size,friendly,immunized,owner_email)
				VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
				"""
		cursor.execute(sql, 
						(self.d_id,self.d_sex, self.d_name, self.d_age, self.d_size,self.d_friendly,self.d_immunized,self.d_owner_email))
		self.d_DbHandler.commit()
		self.d_DbHandler.disconnectFromDb()
		return
    

	