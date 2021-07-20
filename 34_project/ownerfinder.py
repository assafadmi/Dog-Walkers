#-------------------------------------------------------------------------------
# ownerfinder
# -------------------------------------------------------------------------------
# A class to find the owner by email - extract owner data
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------

# import the class Owner to use identity and data members 
import owner
# import the class DbHandler to interact with the database
import db_handler

class OwnerFinder():
    def __init__(self):
        # create DbHandler attribute to use his functions 
        self.of_DbHandler=db_handler.DbHandler()
        # create Owner object
        self.of_RetrievedOwner = owner.Owner()

    # function to find owner in DB by email
    def getOwnerbyemail(self, email):
        self.of_DbHandler.connectToDb()
        cursor = self.of_DbHandler.getCursor()
        #extract selected data from DB
        sql="""
			SELECT email,phone_number,first_name,last_name,city,date_of_birth				
			FROM dog_owners
			WHERE email = %s
			"""
        cursor.execute(sql  ,(email))
        row = cursor.fetchone()
        #set owner data members with selected data from DB
        self.of_RetrievedOwner.o_email = row[0]
        self.of_RetrievedOwner.o_phone_number = row[1]
        self.of_RetrievedOwner.o_first_name = row[2]
        self.of_RetrievedOwner.o_last_name = row[3]
        self.of_RetrievedOwner.o_city = row[4]
        self.of_RetrievedOwner.o_date_of_birth = row[5]
        self.of_DbHandler.disconnectFromDb()
        return self.of_RetrievedOwner
    
    
    
