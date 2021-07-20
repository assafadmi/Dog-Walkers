# -------------------------------------------------------------------------------
# walkrequestfinder
# -------------------------------------------------------------------------------
# A class to find the walk requests in DB by emails 
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------


import walkrequest
# import the class DbHandler to interact with the database
import db_handler
# import the class walk
import walk

class WalkRequestsFinder():
    def __init__(self):
        self.DbHandler=db_handler.DbHandler()


    # a function to find walkrequest in DB by walker email and status 
    def FindWalkRequestsbyemail(self, email, status):
        self.DbHandler.connectToDb()
        cursor = self.DbHandler.getCursor()
        retrievedwalkrequests = []
        sql = 	"""
				SELECT number,walk_request_date,day,part_of_the_day,dog_id
                FROM walk_requests
                WHERE walker_email = %s and status = %s
				"""
        cursor.execute(sql, (email, status))
        rows = cursor.fetchall()
        for walk_request in rows:
            #set each item as walkrequest and set his data members 
            current_walk_request = walkrequest.WalkRequest()
            current_walk_request.number = walk_request[0]
            current_walk_request.walk_request_date = walk_request[1]
            current_walk_request.day = walk_request[2]
            current_walk_request.part_of_the_day = walk_request[3]
            current_walk_request.dog_id = walk_request[4]
            retrievedwalkrequests.append(current_walk_request)
        self.DbHandler.commit()
        self.DbHandler.disconnectFromDb()
        #return a list with selected walkrequests objects
        return retrievedwalkrequests
    

    #a function to show walkers their walk schedule
    def showwalkerschedule(self,email):
        self.DbHandler.connectToDb()
        cursor=self.DbHandler.getCursor()
        retrieved_walks = []
        sql = """
                SELECT day, part_of_the_day, first_name as owner_first_name,
                last_name as owner_last_name, email as owner_email,  phone_number as owner_phone_number, dog_id, name as dog_name
                FROM dog_owners JOIN dogs on dog_owners.email = dogs.owner_email
                JOIN walk_requests on walk_requests.dog_id = dogs.id
                WHERE status = 'approved' and walker_email = %s
            """
        cursor.execute(sql, (email))
        rows = cursor.fetchall()
        for approved_walk in rows:
             #set each item as walk and set his data members 
            current_walk = walk.Walk()
            current_walk.day = approved_walk[0]
            current_walk.part_of_the_day = approved_walk[1]
            current_walk.owner_first_name = approved_walk[2]
            current_walk.owner_last_name = approved_walk[3]
            current_walk.owner_email = approved_walk[4]
            current_walk.owner_phone_number = approved_walk[5]
            current_walk.dog_id = approved_walk[6]
            current_walk.dog_name = approved_walk[7]
            retrieved_walks.append(current_walk)
        self.DbHandler.disconnectFromDb()
        #return a list with selected walks objects
        return retrieved_walks


    # a function to find walker requests by owner email
    def FindWalkRequestsbyowneremail(self, email):
        self.DbHandler.connectToDb()
        cursor = self.DbHandler.getCursor()
        retrivedwalkrequests = []
        sql = """
			    SELECT dog_id, day, part_of_the_day, status, number 
                FROM dog_owners JOIN dogs on dog_owners.email = dogs.owner_email
                JOIN walk_requests on dogs.id = walk_requests.dog_id 
			    WHERE dog_owners.email = %s
			"""
        cursor.execute(sql ,(email))
        rows = cursor.fetchall()
        for walk_request in rows:
            #set each item as walk walkrequest and set his data members 
            current_walk_request = walkrequest.WalkRequest()
            current_walk_request.dog_id = walk_request[0]
            current_walk_request.day = walk_request[1]
            current_walk_request.part_of_the_day = walk_request[2]
            current_walk_request.status = walk_request[3]
            current_walk_request.number = walk_request[4]
            retrivedwalkrequests.append(current_walk_request)
        self.DbHandler.disconnectFromDb()
        # return a list of selected walk request objects
        return retrivedwalkrequests


    # a function to cancel walk request - change status
    def CancelWalkRequestBynumber(self,number):
        self.DbHandler.connectToDb()
        cursor = self.DbHandler.getCursor()
        sql = """
            UPDATE walk_requests
            SET cancellation_date = sysdate(),
            status = 'canceled'
            WHERE number = %s
            """
        cursor.execute(sql,(number))
        self.DbHandler.commit()
        self.DbHandler.disconnectFromDb()
        return