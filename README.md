# Coffee Shop Backend

KongsIsland is a Web Application design to support the captive breeding programmes for gorillas world wide.

The application allows three levels of a user with different permissions for each.  These are:

	1. 	A zookeeper - Can only zoos and gorillas. 
	2.	A vet - Can do everything a Zookeeper can do, can add zoos and gorillas, can modify zoos and gorillas, can delete zoos and gorillas, can view bookings.
	3. 	A Zoo Director - Can do everything a vet can do plus also add and delete bookings.
	
	
The application uses Auth0 to manage the authenticated users and has the following permissions set:

		view:zoos		View available zoos	
		view:gorillas	view available gorillas	
		add:zoos		add zoos	
		add:gorillas	add gorillas	
		delete:zoos		delete zoos	
		delete:gorillas	delete gorillas	
		modify:gorilla	modify gorilla	
		modify:zoo		modify zoo	
		add:bookings	add:bookings	
		delete:bookings	delete:bookings	
		view:bookings	view:bookings


- A rudimentary frontend has been included, but is mainly for testing purposes only.

## Getting Started

- Base URL: The application is hosted on Heroku at the URL of https://kongsisland.herokuapp.com and can be altered to run locally by amending commenting the block labelled database path and uncommenting the same block below. The backend app can then be run `http://127.0.0.1:5000/`


- Authentication: Authentication is required to use the app, non-authenticated users will be required to login.  Authentication is accessed via the frontend through Auth0.

## Key Dependencies
	
	 - [PostgreSql] (https://www.postgresql.org/)  PostgreSQL is a powerful, open source object-relational database.
	
	 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

	 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

	 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 
	 
	 - [POSTMAN] http://www.postman.com) whilst not required for this project, a POSTMAN JSON file is included for testing the authentication processes from Auth0. 

### Installing Dependencies


	1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
	
	2. **PostgreSql** - Follow instrctions to install the latest version of PostgreSql at https://www.postgresql.org/download/.
	
	3. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). For Windows and Linux users, the process is as follows:

		 **Windows users in Bash**

		Ensure you're in the Backend folder in Bash and follow the following.

		``` bash
		Python -m venv venv
		source venv/scripts/activate
		```
		
		**Linux users in Bash**
		
		Ensure you're in the Backend folder in Bash and follow the following.
		``` bash
		Python -m venv venv
		source venv/bin/activate	
		```
	4. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
	
	```bash
	pip install -r requirements.txt
	```
	
	This will install all of the required packages included within the `requirements.txt` file.

## Database Description

	5.	The database is made up of three tables, Zoos - for the listing of individual Zoos, Gorillas - for the listing of individual gorillas and Bookings, a table with foreginkeys linked to relationship keys in Zoos and Gorillas.

## Local Database setup
	 
	6.	Start Postgres, in windows this is achieved by typing the following in a bash window:
		
		pg_ctl -d "C:\program files\postgresql\10\data" start  	substitute the number 10 for the version number of postgresql you have installed.
		
		Creating the database is an automated process.  Within the App.py application uncomment line 48 "db_drop_and_create_all() and a new local database will be created with some sample data. 
		
## Running the application

	7. To run the app online, simply access https://kongsisland.herokuapp.com and logging in.
	
	8. To run the programme locally:

			Each time you open a new terminal session, run:

			```bash
			export FLASK_APP=app.py;
			```

			To run the server, execute:

			```bash
			pg_ctl -D "c:\program files\postgresql\10\data" start
			flask run --reload
			```
			
			The `--reload` flag will detect file changes and restart the server automatically.
			
	9. Open a web-browser and point it to http://localhost:5000
	
## Error handling

	10.	A number of error checking has been made available which are described below:
			a.	A Postman collection JSON for testing authorisations on a local database has been made available, called konsisland.postman_collection.json.  Import this into Postman and run the tests.  The individual keys may have expired, in which case contact the author to supply renewed keys.
			
			b. A Unittest has been supplied and is configured to carry out tests, detailed in para XXX.  The Unittest, called kongsisland_unittest.py is currently configured to test the online version of the application.  To test locally, carry out the local installs as directed above and comment out lines 25-30 in the py file and uncomment lines 32-38.  This will ensure the test is aimed at the local machine.

	

	Errors will be returned in the following json format:
	
		```
		json
			  {
			   'success': False,
			   'error': 404,
			   'message': 'Resource not found, we searched everywhere'
			  }
		```
		
	11.	The error codes currently returned are:
	
	* 400 - Bad Request Error
	* 401 - Unauthorised
	* 404 - Resource not Found Error
	* 500 - Internal Server Error
	* 422 - Unprocessable Error
	* AuthError - handled by Auth.py to confirm if a user has correct permissions.
	
	12. Authentication processes were checked using Postman (https://www.postman.com) and through the used of the unittest mention in para 9b above.  The included postman and unittest test against the Endpoints listed below.
	
##	Endpoints

	13.	The following endpoints are used within the App:

	** GET / zoos
	-	General:
		Displays zoos to logged in users of type 'zookeeper', 'vet' and 'zoodirector'.
	
	** POST / zoos/search
	-	General:
		Allows for the searching of zoos and allowable by users of type 'zookeeper', 'vet' and 'zoodirector'.
		
	** GET /gorillas
	-	General:
		Lists gorillas and their future bookings to worldwide zoos.  Accessible by users of type 'zookeeper', 'vet' and 'zoodirector'.
		
	** POST /gorillas/search
	-	General:
		Allows for the searching of gorillas and allowable by users of type 'zookeeper', 'vet' and 'zoodirector'.
		
	** POST /zoos/create
		General:
		Allows for the posting of new zoos and allowable by users of type 'vet' and 'zoodirector'.
		
	** POST /gorillas/create
		General:
		Allows for the posting of new gorillas and allowable by users of type 'vet' and 'zoodirector'.
		
	** PATCH /zoos/<int:id>/edit
		General:
		Allows for the editing of zoos and allowable by users of type 'vet' and 'zoodirector'.	
		
	** PATCH /gorillas/<int:id>/edit
		General:
		Allows for the editing of gorillas and allowable by users of type 'vet' and 'zoodirector'.
		
	** DELETE /zoos/<int:id>/delete
		General:
		Allows for the deletion of zoos and allowable by users of type 'vet' and 'zoodirector'.
	
	** DELETE /gorillas/<int:id>/delete
		General:
		Allows for the deletion of zoos and allowable by users of type 'vet' and 'zoodirector'.
		
	** POST /bookings/create
		General:
		Allows for the posting of new bookings and allowable by users of type 'zoodirector'.

	** POST /bookings/<int:id>delete
		General:
		Allows for the deleting of bookings and allowable by users of type 'zoodirector'.
	
	
### Setup Auth0

	14. Auth0 (https://auth0.com) is an external website that can provide for the management of users and permissions and was chosen as this Webapp's authentication method.  It has been set up using the following details:
	```
		AUTH0_DOMAIN = 'fsnd-tgrahame.eu.auth0.com'
		ALGORITHMS = ['RS256']
		API_AUDIENCE = 'kongsisland'
	```
## Authors
	- 	The rudimentary front end was modified from a previous lesson created by Udacity.  With this exception the entire application was created by Tim Grahame