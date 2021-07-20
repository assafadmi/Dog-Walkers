# -------------------------------------------------------------------------------
# owner
# -------------------------------------------------------------------------------
# A class to classify user as owner,walker, new user - serch in DB
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------

#import db handler to interact with data base
import db_handler


class FindUser():
    def __init__(self):
        self.DbHandler=db_handler.DbHandler()
    
    # a function to classify the user
    def whatkindofuser(self,email):
        self.DbHandler.connectToDb()
        cursor = self.DbHandler.getCursor()
        # searching in dog owners table
        sql_1="""
			SELECT count(*)				
			FROM dog_owners
			WHERE email = %s
			"""
        cursor.execute(sql_1  ,(email))
        row_1 = cursor.fetchone()
        in_owners_table = row_1[0]
        # searching in dog walkers table
        sql_2="""
			SELECT count(*)				
			FROM dog_walkers
			WHERE email = %s
			"""
        cursor.execute(sql_2  ,(email))
        row_2 = cursor.fetchone()
        in_walkers_table = row_2[0]
        self.DbHandler.disconnectFromDb()
        if in_owners_table == 1:
            return "he is a owner"
        elif in_walkers_table == 1:
            return "he is a walker"
        # he is new user
        else:
            return 