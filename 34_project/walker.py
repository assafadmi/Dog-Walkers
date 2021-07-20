# -------------------------------------------------------------------------------
# walker
# -------------------------------------------------------------------------------
# A class to manage the walkers and a class for their availability times-create and save in the DB
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------


# import the class DbHandler to interact with the database
import db_handler

class Walker():
    def __init__(self):
         # create DbHandler attribute to use his functions 
        self.w_DbHandler=db_handler.DbHandler()
        # create data members of the class 
        self.w_email = ""
        self.w_first_name = ""
        self.w_last_name = ""
        self.w_seniority = ""
        self.w_city = ""
        self.w_street = ""
        self.w_house_number = ""
        self.w_small_price = ""
        self.w_medium_price = ""
        self.w_large_price = ""
        self.w_phone_number = ""
        self.w_availablity_times = []

 # function to insert walker into database
    def insertToDb(self):
        self.w_DbHandler.connectToDb()
        cursor = self.w_DbHandler.getCursor()
        sql = 	"""
                INSERT INTO dog_walkers(email,first_name,last_name,seniority,city,street,house_number,
                small_price,medium_price,large_price,phone_number) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(sql,(self.w_email, self.w_first_name,self.w_last_name, self.w_seniority, self.w_city.upper(), self.w_street, self.w_house_number, self.w_small_price, self.w_medium_price, self.w_large_price, self.w_phone_number))
        self.w_DbHandler.commit()
        self.w_DbHandler.disconnectFromDb()
        return

class AvailabilityTime():
    def __init__(self):
        # create DbHandler as attribute to use his functions to connect to DB
        self.at_DbHandler = db_handler.DbHandler()
        # create data members of the class 
        self.day = ""
        self.part_of_the_day = ""
        self.email = ""

 # function to insert AvailabilityTime into database
    def insertToDb(self):
        self.at_DbHandler.connectToDb()
        curser = self.at_DbHandler.getCursor()
        sql = """
                INSERT INTO availability_times(day,part_of_the_day,email)
                VALUES(%s,%s,%s)
                """
        curser.execute(sql,(self.day,self.part_of_the_day,self.email))
        self.at_DbHandler.commit()
        self.at_DbHandler.disconnectFromDb()
        return
    
     # a function to find all AvailabilityTime in chosen day and part of the day
    def findavailablewalkers(self,day,part_of_the_day,city):
        walkers = []
        self.at_DbHandler.connectToDb()
        cursor = self.at_DbHandler.getCursor()
        #extract selected data from DB 
        sql="""
			SELECT dog_walkers.email,phone_number,first_name,last_name,small_price,medium_price,large_price	
			FROM availability_times join dog_walkers
            ON availability_times.email = dog_walkers.email
			WHERE day = %s and part_of_the_day = %s and city = %s 
			"""
        cursor.execute(sql  ,(day,part_of_the_day,city))        
        rows = cursor.fetchall()
        # iterate all the selected rows from DB
        for available_walker in rows:
            # create a Walker identity and set data members
            walker = Walker()
            walker.w_email = available_walker[0]
            walker.w_phone_number = available_walker[1]
            walker.w_first_name = available_walker[2]
            walker.w_last_name = available_walker[3]
            walker.w_small_price = available_walker[4]
            walker.w_medium_price = available_walker[5]
            walker.w_large_price = available_walker[6]
            walkers.append(walker)
        self.at_DbHandler.disconnectFromDb()
        # return list of Walker objects
        return walkers        
