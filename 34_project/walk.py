# -------------------------------------------------------------------------------
# walk
# -------------------------------------------------------------------------------
# A class to add owners information to walk requests and show them on-
# walkers schedule - create  
#-------------------------------------------------------------------------
# Authors:       Edan Sadeh, Barak Nakash, Assaf Admi
# Last updated: 29.12.2020
#-------------------------------------------------------------------------

class Walk():
    def __init__(self):
        # create data members of the class  
        self.owner_email = ""
        self.day = ""
        self.part_of_the_day = ""
        self.owner_first_name = ""
        self.owner_last_name = ""
        self.owner_phone_number = ""
        self.dog_id = ""
        self.dog_name = ""