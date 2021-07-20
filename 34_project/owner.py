# -------------------------------------------------------------------------------
# owner
# -------------------------------------------------------------------------------
# A class to manage the owners-create and save in the DB
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------


# import the class DbHandler to interact with the database
import db_handler

class Owner():
    def __init__(self):
		# create DbHandler attribute to use his functions 
        self.o_email = ""
        self.o_DbHandler=db_handler.DbHandler()
         # create data members of the class  
        self.o_phone_number = ""
        self.o_city = ""
        self.o_first_name = ""
        self.o_last_name = ""
        self.o_date_of_birth = ""

# function to insert owner into database
    def insertToDb(self):
		self.o_DbHandler.connectToDb()
		cursor=self.o_DbHandler.getCursor()
		sql = 	"""
				INSERT INTO dog_owners(email,phone_number,city,first_name,last_name,date_of_birth) 
				VALUES(%s,%s,%s,%s,%s,%s)
				"""
		cursor.execute(sql, 
						(self.o_email,self.o_phone_number, self.o_city.upper(), self.o_first_name, self.o_last_name, self.o_date_of_birth))
		self.o_DbHandler.commit()
		self.o_DbHandler.disconnectFromDb()
		return
	