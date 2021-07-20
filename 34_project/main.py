# ------------------------------------------------------
# dog to walk project
# ------------------------------------------------------
# The application connects between dog owners and dog walkers
# who live in the same city. Dog owners can enroll their dog
# to the website and find a dog walker for them. Dog walkers
# have availability times, and they get to decide which walk requests
# to confirm or decline.
# ------------------------------------------------------
# Authors       - Assaf Admi, Edan Sadeh, Barak Nakash
# Last updated - 30.12.2020
# ------------------------------------------------------

# import libraries and classes
import webapp2
import jinja2
import os
from google.appengine.api import users
import db_handler
import owner
import ownerfinder
import walker
import walkerfinder
import dog
import dogfinder
import walkrequest
import walkrequestfinder
import finduser
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
# -------------------------------------------------------------
# class to show the home page of the website
# -------------------------------------------------------------
class HomePage(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the home page
    def get(self):
        # Display the form
		template = jinja_environment.get_template('home_page.html')
		self.response.write(template.render())

# -------------------------------------------------------------
# class to show the goodbye page after logout
# -------------------------------------------------------------
class SeeYouSoon(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the goodbye_page
    def get(self):
        # Display the form
		template = jinja_environment.get_template('goodbye_page.html')
		self.response.write(template.render())

# -------------------------------------------------------------
# class to login to google account
# -------------------------------------------------------------
class Login(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()  
        # if the user object exists (the user is logged in to google)
        if user:
            self.redirect('/find_user')
        # The user object doesn't exist ( the user is not logged to google)
        # we will ask him to login and
        # provide the URI of the find user class
        else:      
            self.redirect(users.create_login_url('/find_user'))

# -------------------------------------------------------------
# class to logout from the website
# -------------------------------------------------------------
class Logout(webapp2.RequestHandler):
	def get(self):
        # if the user is logged in - we will perform log out
		user = users.get_current_user()
		if user:
            # force the user to logout and redirect him afterward to home page
			self.redirect(users.create_logout_url('/see_you_soon'))
		else:
			self.redirect('/see_you_soon')

# -------------------------------------------------------------
# class to check who is the user.
# -------------------------------------------------------------
class FindUser(webapp2.RequestHandler):
	def get(self):
		#find user email
		user = users.get_current_user()
		email = user.email()
		# check if the user already exists in the database,
		# and if he is a owner or a walker(by using whatkindofuser method)
		# redirect him to his menu
		# (by using ExistDogOwner/ExistDogwalker/NewUserMainPage classes)		
		if finduser.FindUser().whatkindofuser(email) == 'he is a owner':
			self.redirect('/exist_dog_owner')
		elif finduser.FindUser().whatkindofuser(email) == 'he is a walker':
			self.redirect('/exist_dog_walker')
		else:
			self.redirect('/new_user_main_page')
		
# -------------------------------------------------------------
# class to create the new user main page.
# only first time users will use this page.
# -------------------------------------------------------------
class NewUserMainPage(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "new_user_main_page" form
    def get(self):
        # Display the form
		template = jinja_environment.get_template('new_user_main_page.html')
		self.response.write(template.render())

# -------------------------------------------------------------
# class to create the form of a new owner
# and submit it (by clicking Send)
# -------------------------------------------------------------
class OwnerSignUp(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "owner_sign_up" form
	def get(self):
      # Display the form
		template = jinja_environment.get_template('owner_sign_up.html')
		self.response.write(template.render())

# -------------------------------------------------------------
# class to create the form of a new walker
# and submit it (by clicking Send)
# -------------------------------------------------------------
class WalkerSignUp(webapp2.RequestHandler):
    # When we receive an HTTP GET request - display the "walker_sign_up" form
	def get(self):
      # Display the form
		template = jinja_environment.get_template('walker_sign_up.html')
		self.response.write(template.render())

# -------------------------------------------------------------
# class to create the form of a new dog
# and submit it (by clicking Send)
# -------------------------------------------------------------
class DogsEnroll(webapp2.RequestHandler):
	def get(self):
      # Display the form
		template = jinja_environment.get_template('dogs_enroll.html')
		self.response.write(template.render())

# -----------------------------------------------------------------------------
# When we receive an HTTP POST request -we get the parameters from the post request.
# We insert the owner into the database and display the owner menu.
# The post method will be called when someone clicks
# submit button (send) in the owner_sign_up form
# -----------------------------------------------------------------------------
class OwnerDetailsSent(webapp2.RequestHandler):
	def post(self):
		owner_obj = owner.Owner()
		#Request data from the POST request
		owner_obj.o_email = self.request.get('owner_email')
		owner_obj.o_phone_number = self.request.get('owner_phone_number')
		owner_obj.o_city = self.request.get('owner_city')
		owner_obj.o_first_name = self.request.get('owner_first_name')
		owner_obj.o_last_name = self.request.get('owner_last_name')
		owner_obj.o_date_of_birth = self.request.get('owner_date_of_birth')
		#----------------------------------------
		# Add the Owner into the database
		#----------------------------------------
		owner_obj.insertToDb()
		# redirect to ExistDogOwner class which will display the owner menu
		self.redirect('/exist_dog_owner')

# -----------------------------------------------------------------------------
# When we receive an HTTP POST request -we get the parameters from the post request.
# We insert the walker into the database and display the walker menu.
# The post method will be called when someone clicks
# submit button (send) in the walker_sign_up form
# -----------------------------------------------------------------------------
class WalkerDetailsSent(webapp2.RequestHandler):
	def post(self):
		walker_obj = walker.Walker()
		days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
		parts_of_the_day = ['morning','noon','evening']
		#Request data from the POST request
		walker_obj.w_email = self.request.get('dog_walker_email')
		walker_obj.w_first_name = self.request.get('dog_walker_first_name')
		walker_obj.w_last_name = self.request.get('dog_walker_last_name')
		walker_obj.w_seniority = self.request.get('dog_walker_seniority')
		walker_obj.w_city = self.request.get('dog_walker_city')
		walker_obj.w_street = self.request.get('dog_walker_street')
		walker_obj.w_house_number = self.request.get('dog_walker_house_number')
		walker_obj.w_small_price = self.request.get('dog_walker_small_price')
		walker_obj.w_medium_price = self.request.get('dog_walker_medium_price')
		walker_obj.w_large_price = self.request.get('dog_walker_large_price')
		walker_obj.w_phone_number = self.request.get('dog_walker_phone')
		# create list of availability times for the walker
		for day in days:
			for part_of_the_day in parts_of_the_day:
				# if the user available in one of the parts of the
				# days in the week, add this time to his availablity times list
				if self.request.get(day + '_' + part_of_the_day) == 'yes':
					availability_time = walker.AvailabilityTime()
					availability_time.day = day
					availability_time.part_of_the_day = part_of_the_day
					availability_time.email = self.request.get('dog_walker_email')
					walker_obj.w_availablity_times.append(availability_time)
		#----------------------------------------
		# Add the Walker into the database
		#----------------------------------------
		walker_obj.insertToDb()
		#----------------------------------------
		# Add the Walker availability times into the database
		#----------------------------------------
		for availability_time in walker_obj.w_availablity_times:
					availability_time.insertToDb()
		# redirect to ExistDogWalker class which will display the walker menu
		self.redirect('/exist_dog_walker')

# -------------------------------------------------------------------------------------
# When we receive an HTTP POST request -we get the parameters from the post request.
# We insert the dog into the database and display the owner menu.
# The post method will be called when someone clicks
# submit button (send) in the dogs_enroll form
# -------------------------------------------------------------------------------------
class DogDetailsSent(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		dog_obj = dog.Dog()
		#Request data from the POST request
		dog_obj.d_id = self.request.get('dog_id')
		dog_obj.d_sex = self.request.get('dog_sex')
		dog_obj.d_name = self.request.get('dog_name')
		dog_obj.d_age = self.request.get('dog_age')
		dog_obj.d_size = self.request.get('dog_size')
		dog_obj.d_friendly = self.request.get('dog_friendly')
		dog_obj.d_immunized = self.request.get('dog_immunized')
		dog_obj.d_owner_email = user.email()
		#----------------------------------------
		# Add the dog into the database
		#----------------------------------------
		dog_obj.insertToDb()
		# redirect to ExistDogOwner class which will display the owner menu
		self.redirect('/exist_dog_owner')

# ------------------------------------------------------------------
# Class to find out who is the owner and display him his owner menu
# ------------------------------------------------------------------
class ExistDogOwner(webapp2.RequestHandler):	
	def get(self):
		user = users.get_current_user()
		email = user.email()
		owner = ownerfinder.OwnerFinder().getOwnerbyemail(email)
		template = jinja_environment.get_template('owner_menu.html')
		parameters_for_template = {	'current_owner': owner} 
		self.response.write(template.render(parameters_for_template))

# ---------------------------------------------------------------------
# Class to find out who is the walker and display him his walker menu
# ---------------------------------------------------------------------
class ExistDogWalker(webapp2.RequestHandler):	
	def get(self):
		user = users.get_current_user()
		email = user.email()
		walker = walkerfinder.WalkerFinder().getWalkerbyemail(email)
		template = jinja_environment.get_template('walker_menu.html')
		parameters_for_template = {	'current_walker': walker} 
		self.response.write(template.render(parameters_for_template))

# -------------------------------------------------------------
# class to create the form of a new walk request.
# and submit it (by clicking Send).
# the dog owner will have to choose one of his dogs,
# and the time in the week for the walk.
# -------------------------------------------------------------
class NewWalkRequest(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		email = user.email()
		dogs = dogfinder.DogsFinder().getdogsbyowneremail(email)
		template = jinja_environment.get_template('new_walk_request.html')
		parameters_for_template = {	'dogs_list': dogs} 
		self.response.write(template.render(parameters_for_template))

# --------------------------------------------------------------------------
# When we receive an HTTP POST request -we get the parameters from the post request.
# this class display the available dog walkers details 
# in the owner's city (for the specific dog size)
# will desplay one of:
# choose_dog_walker_large/choose_dog_walker_medium/choose_dog_walker_small
# the owner will choose a dog walker and click send.
# --------------------------------------------------------------------------
class WalkRequestSent1(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		email = user.email()
		walk_request_obj = walkrequest.WalkRequest()
		#Request data from the POST request
		walk_request_obj.dog_id = self.request.get('dog_id')
		walk_request_obj.day = self.request.get('day')
		walk_request_obj.part_of_the_day = self.request.get('part_of_the_day')
		owner = ownerfinder.OwnerFinder().getOwnerbyemail(email)
		city = owner.o_city
		dog = dogfinder.DogsFinder().getdogbydogid(walk_request_obj.dog_id)
		availablewalkers = walker.AvailabilityTime().findavailablewalkers(walk_request_obj.day,walk_request_obj.part_of_the_day,city)
		if dog.d_size == 'small':
			template = jinja_environment.get_template('choose_dog_walker_small.html')
		if dog.d_size == 'medium':
			template = jinja_environment.get_template('choose_dog_walker_medium.html')
		if dog.d_size == 'large':
			template = jinja_environment.get_template('choose_dog_walker_large.html')					
		parameters_for_template = {	'availablewalkers': availablewalkers,'day':walk_request_obj.day,'part_of_the_day': walk_request_obj.part_of_the_day,"dog" : dog } 
		self.response.write(template.render(parameters_for_template))

# --------------------------------------------------------------------------
# When we receive an HTTP POST request -we get the parameters from the post request.
# We insert the walk request into the database and display the owner menu.
# The post method will be called when someone clicks
# submit button (send) in the choose_dog_walker_large/medium/small form
# --------------------------------------------------------------------------
class WalkRequestSent2(webapp2.RequestHandler):
	def post(self):
		walk_request_obj = walkrequest.WalkRequest()
		walk_request_obj.day = self.request.get('day')
		walk_request_obj.part_of_the_day = self.request.get('part_of_the_day')
		walk_request_obj.dog_id = self.request.get('dog.d_id')
		walk_request_obj.walker_email = self.request.get('walker_email')
		walk_request_obj.insertToDb()
		self.redirect('/exist_dog_owner')

# -----------------------------------------
# Displays to the walker his walk requests
# -----------------------------------------
class ShowWalkRequests(webapp2.RequestHandler):
	def get(self):
		# get the walker emai
		user = users.get_current_user()
		email = user.email()
		# find his waiting walk requests by using the method FindWalkRequestsbyemail
		walker_walk_requests = walkrequestfinder.WalkRequestsFinder().FindWalkRequestsbyemail(email,'waiting')
		# display the walker's waiting walk requests
		template = jinja_environment.get_template('show_walk_requests.html')
		parameters_for_template = {	'walker_walk_requests': walker_walk_requests} 
		self.response.write(template.render(parameters_for_template))

# -------------------------------------------------------------------------
# When we receive an HTTP POST request -we get the parameters from the post request.
# class to update the walk requests status.
#(when the walker confirm/decline/keep waiting his waiting walk requests)
# -------------------------------------------------------------------------
class UpdateWalkRequestStatus(webapp2.RequestHandler):
	def post(self):
		# get the walker email
		user = users.get_current_user()
		email = user.email()
		# find his waiting walk requests by using the method FindWalkRequestsbyemail
		walker_walk_requests = walkrequestfinder.WalkRequestsFinder().FindWalkRequestsbyemail(email,'waiting')
		# update every walk request status according to the walker desicions
		for walk_request in walker_walk_requests:
			#get the walker decision from the post request
			status_update = self.request.get(str(walk_request.number))
			if status_update == 'yes':
				walk_request.update_status(email, 'approved')
			elif status_update == 'no':
				walk_request.update_status(email, 'declined')
		# redirect to ExistDogWalker class which will display the walker menu
		self.redirect('/exist_dog_walker')

# -----------------------------------------
# Displays to the walker his schedule
# -----------------------------------------
class ShowWalkerSchedule(webapp2.RequestHandler):
	def get(self):
		# get the walker email
		user = users.get_current_user()
		email = user.email()
		days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
		# find the walker's confirmed walks by using the method showwalkerschedule
		walker_approved_walks = walkrequestfinder.WalkRequestsFinder().showwalkerschedule(email)
		# display the walker's schedule
		template = jinja_environment.get_template('walker_schedule.html')
		parameters_for_template = {'walker_approved_walks': walker_approved_walks,'days':days } 
		self.response.write(template.render(parameters_for_template))

# -----------------------------------------
# Displays to the owner his walk requests
# -----------------------------------------
class ShowOwnerRequests(webapp2.RequestHandler):
	def get(self):
 		# get the owner email
		user = users.get_current_user()
		email = user.email()
		# find his walk requests by using the method FindWalkRequestsbyowneremail
		owner_requests = walkrequestfinder.WalkRequestsFinder().FindWalkRequestsbyowneremail(email)
		# display the owner's walk requests
		template = jinja_environment.get_template('owner_requests.html')
		parameters_for_template = {'owner_requests': owner_requests} 
		self.response.write(template.render(parameters_for_template))

# -------------------------------------------------------------------------
# When we receive an HTTP POST request -we get the parameters from the post request.
# class to cancel the walk requests status in the data base
#(when the owner cancels one of his walk requests)
# -------------------------------------------------------------------------
class CancelWalkRequest(webapp2.RequestHandler):
	def post(self):
		# get the owner email
		user = users.get_current_user()
		email = user.email()
		# find his walk requests by using the method FindWalkRequestsbyowneremail
		owner_requests = walkrequestfinder.WalkRequestsFinder().FindWalkRequestsbyowneremail(email)
		for walk_request in owner_requests:
			# get the owner decision from the post request
			cancel = self.request.get(str(walk_request.number))
			# if the owner decided to cancel the walk request,
			# change the walk request status to 'canceled'
			# by using the method CancelWalkRequestBynumber
			if cancel == 'yes':
				walkrequestfinder.WalkRequestsFinder().CancelWalkRequestBynumber(walk_request.number)
		# redirect to ExistDogOwner class which will display the owner menu
		self.redirect('/exist_dog_owner')

# -------------------------------------------------------------
# Routing
# -------------------------------------------------------------
app = webapp2.WSGIApplication([('/find_user',FindUser),
								('/see_you_soon',SeeYouSoon),
								('/exist_dog_walker', ExistDogWalker),
								('/login', Login),
								('/', HomePage),
								('/logout', Logout),
								('/new_user_main_page', NewUserMainPage),
                                ('/dog_owner', OwnerSignUp),
								('/dog_walker', WalkerSignUp),
								('/exist_dog_owner', ExistDogOwner),
								('/owner_details_sent', OwnerDetailsSent),
								('/walker_details_sent', WalkerDetailsSent),
								('/dog_details_sent',DogDetailsSent),
								('/dogs_enroll', DogsEnroll),
								("/new_walk_request",NewWalkRequest),
								("/walk_request_sent_1",WalkRequestSent1),
								("/walk_request_sent_2",WalkRequestSent2),
								("/show_walk_requests",ShowWalkRequests),
								("/update_walk_requests_status",UpdateWalkRequestStatus),
								("/show_walker_schedule",ShowWalkerSchedule),
								('/show_owner_requests',ShowOwnerRequests),
								('/cancel_walk_request',CancelWalkRequest)
							    ],
								debug=True)



