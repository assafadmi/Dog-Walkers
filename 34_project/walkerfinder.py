# -------------------------------------------------------------------------------
# walkerfinder
# -------------------------------------------------------------------------------
# A class to find the walker by email - extract walker data
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------

# import the class walker to use identity and data members
import walker
# import the class DbHandler to interact with the database
import db_handler
class WalkerFinder():
    def __init__(self):
        # create DbHandler attribute to use his functions 
        self.wf_DbHandler=db_handler.DbHandler()
        # create walker object
        self.wf_RetrievedWalker = walker.Walker()


      # function to find owner in DB cy email
    def getWalkerbyemail(self, email):
        self.wf_DbHandler.connectToDb()
        cursor = self.wf_DbHandler.getCursor()
         #extract selected data from DB 
        sql="""
			SELECT email,first_name,last_name,seniority,city,street,house_number,
                small_price,medium_price,large_price,phone_number from dog_walkers
			WHERE email = %s
			"""
        cursor.execute(sql  ,(email))
        row = cursor.fetchone()
         #set owner data members with selected data from DB
        self.wf_RetrievedWalker.w_email = row[0]
        self.wf_RetrievedWalker.w_first_name = row[1]
        self.wf_RetrievedWalker.w_last_name = row[2]
        self.wf_RetrievedWalker.w_seniority = row[3]
        self.wf_RetrievedWalker.w_city = row[4]
        self.wf_RetrievedWalker.w_street = row[5]
        self.wf_RetrievedWalker.w_house_number = row[6]
        self.wf_RetrievedWalker.w_small_price = row[7]
        self.wf_RetrievedWalker.w_medium_price = row[8]
        self.wf_RetrievedWalker.w_large_price = row[9]
        self.wf_RetrievedWalker.w_phone_number = row[10]
        self.wf_DbHandler.disconnectFromDb()
        return self.wf_RetrievedWalker