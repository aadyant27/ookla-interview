# Event Management RESTful APIs

### How to run the project
1. Create a virtual env. `python -m venv <name>`
2. Activate the environment `source <env_name>/bin/activate`
3. Install requirements.txt file `pip install -r requirements.txt`
4. Run the server `python manage.py runserver`

## Implementatation Description
* The project contains 2 application **users** & **events**
  
* user app handles all the user related data which includes:
    1. Listing all the users
    2. Creating the users/admin-users
    3. Generating auth token for the users
       
* events app handles all event management related data, namely:
    1. Listing all events
    2. Creating new events
    3. Getting specific event
    4. Booking tickets for a specific event
    5. Listing of all the bookings of Users for different events
       
* **ASSUMPTION**: There is no distinction between any 2 tickets for an event i.e. there are 2 types of ticket management services, one in which each ticket is unique & holds different value (like a movie theatre), other in which all tickets are same in the experience they provide i.e. entry through the gates(like a waterpark). We assume the latter.

* Test classes have been implemented in test.py file for both the apps.

* **ADDITIONAL FEATURES ADDED**
  1. Creation of Auth token(JWT) for user verification.
  2. Surge Pricing in case of Fast-filling events
  3. NO HOARDING i.e. user with same credentials cannot buy more than 4 tickets. Also restricting multiple buys from the same user
  4. Booking can only be done by registered users.
  5. Geocode API(Google) to find Latitude, Longitude which can then used by frontend to render Google Maps in frontend
 
* Swagger Docs: /api/swagger/
