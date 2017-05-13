#!/home/jhm4/mypython/bin/python
import MySQLdb
import datetime
from geopy.geocoders import Nominatim
import pandas as pd


db = MySQLdb.connect(host='localhost', user='jhm4_john',passwd='skittles',db='jhm4_lab2')
cur = db.cursor()

###################################################################################
# This commented out section would function in a separate program as a process
# to enter into our "Event" database events that users register on our website.
# The addresses that are assigned to the variables "event#" would instead be 
# provided through url arguments submitted in POST format from one of our html
# pages.
###################################################################################

#event1= "20 Prospect Ave, Princeton, NJ 08540"
#event2= "65 Olden St, Princeton, NJ 08540"
#event3= "10 Palmer Square, Princeton, NJ 08542"
#event4= "55 E 52nd St, New York, NY 10055"
#event5= "200 West St, New York, NY 10282"

#geolocator1 = Nominatim()
#geolocator2 = Nominatim()
#geolocator3 = Nominatim()
#geolocator4 = Nominatim()
#geolocator5 = Nominatim()

#location1 = geolocator1.geocode(event1)
#location2 = geolocator2.geocode(event2)
#location3 = geolocator3.geocode(event3)
#location4 = geolocator4.geocode(event4)
#location5 = geolocator5.geocode(event5)

#date1=str(datetime.date(2017,05,12))
#date2=str(datetime.date(2017,11,11))
#date3=str(datetime.date(2017,05,28))
#date4=str(datetime.date(2017,05,15))
#date5=str(datetime.date(2017,05,14))

#time=str(datetime.time())

#cur.execute("INSERT INTO finalEvents (eventName, address, eventDate, startTime, latitude, longitude, Pass, Email) VALUES ('Event 1', \'" + event1+"\', \'"+date1+"\', \'"+time+"\', \'"+ str(location1.latitude) +
#	"\', \'" +str(location1.longitude) +"\', 'hello1', 'jhm41@princeton.edu')")
#cur.execute("INSERT INTO finalEvents (eventName, address, eventDate, startTime, latitude, longitude, Pass, Email) VALUES ('Event 2', \'" + event2+"\', \'"+date2+"\', \'"+time+"\', \'"+ str(location2.latitude) +
#	"\', \'" +str(location2.longitude) +"\', 'hello2', 'jhm42@princeton.edu')")
#cur.execute("INSERT INTO finalEvents (eventName, address, eventDate, startTime, latitude, longitude, Pass, Email) VALUES ('Event 3', \'" + event3+"\', \'"+date3+"\', \'"+time+"\', \'"+ str(location3.latitude) +
#	"\', \'" +str(location3.longitude) +"\', 'hello3', 'jhm43@princeton.edu')")
#cur.execute("INSERT INTO finalEvents (eventName, address, eventDate, startTime, latitude, longitude, Pass, Email) VALUES ('Event 4', \'" + event4+"\', \'"+date4+"\', \'"+time+"\', \'"+ str(location4.latitude) +
#	"\', \'" +str(location4.longitude) +"\', 'hello4', 'jhm44@princeton.edu')")
#cur.execute("INSERT INTO finalEvents (eventName, address, eventDate, startTime, latitude, longitude, Pass, Email) VALUES ('Event 5', \'" + event5+"\', \'"+date5+"\', \'"+time+"\', \'"+ str(location5.latitude) +
#	"\', \'" +str(location5.longitude) +"\', 'hello5', 'jhm45@princeton.edu')")

##########################################################################################

###################################################################################
# This section would be the script that serves the "Events Near Me" funciton on
# website. The address assigned to the variable "query" would be provided as url
# arguments submitted in POST format from our html page using the address saved as
# our user's home address. In the future, we would probably switch to Google's 
# location API versus Nominatim because it is a little more accurate.
###################################################################################


geolocatorSearch = Nominatim()
query = "91 University Pl, Princeton, NJ 08540"
locationSearch = geolocatorSearch.geocode(query)
searchLatitude = locationSearch.latitude
searchLongitude = locationSearch.longitude

df = pd.read_sql("SELECT * FROM finalEvents WHERE latitude <=\'" + str(searchLatitude+.2763) +
	 "\' AND latitude >=\'" + str(searchLatitude-.2763)+"\' AND longitude <=\'" + str(searchLongitude+0.5864) +
	 "\' AND longitude >=\'" + str(searchLongitude-.5864) + "\'", con=db)


event = df['eventName']
address = df['address']
dates = df['eventDate']
times = df['startTime']

eventS = pd.Series(event)
count = eventS.size

# We would add a lot more output through print statements to display everything in an html page with
# a lot of CSS markups added.

i=0
while i < count:
	print str(eventS[i])
	i=i+1



db.close()

