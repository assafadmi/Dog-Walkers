
#-------------------------------------------------------------------------------
# dogsfinder
# -------------------------------------------------------------------------------
# A class to find the dogs - extract dogs data drom DB
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------import owner

#import db handler to interact with DB
import db_handler
# import dog to use his functions
import dog

class DogsFinder():
    def __init__(self):
        self.df_DbHandler=db_handler.DbHandler()
        self.df_RetrievedDogs = []
       
    # function to find dog by owners email
    def getdogsbyowneremail(self,email):
        self.df_DbHandler.connectToDb()
        cursor = self.df_DbHandler.getCursor()
        sql = """
            SELECT id, name, size FROM dogs
            WHERE owner_email = %s
            """
        cursor.execute(sql  ,(email))
        rows = cursor.fetchall()
        for dogo in rows:
            # set each slected item as dog and set his data members
            current_dog = dog.Dog()
            current_dog.d_id = dogo[0]
            current_dog.d_name = dogo[1]
            current_dog.d_size = dogo[2]
            self.df_RetrievedDogs.append(current_dog)
        self.df_DbHandler.disconnectFromDb()
        # return a list of dog objects 
        return self.df_RetrievedDogs
    
    # function to find dog by dog id
    def getdogbydogid(self,id):
        self.df_DbHandler.connectToDb()
        cursor = self.df_DbHandler.getCursor()
        sql = """
            SELECT id, name, size FROM dogs
            WHERE id = %s
            """
        cursor.execute(sql  ,(id))
        row = cursor.fetchone()
        # set the selected item as dog and set his data members
        current_dog = dog.Dog()
        current_dog.d_id = row[0]
        current_dog.d_name = row[1]
        current_dog.d_size = row[2]
        self.df_DbHandler.disconnectFromDb()
        # return slected dog
        return current_dog  