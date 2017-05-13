#!/home/jhm4/mypython/bin/python
import MySQLdb
import datetime
from geopy.geocoders import Nominatim
import pandas as pd
from geopy.distance import vincenty


### This program is designed to group all possible travelers together in shared trips
### to a specific event which would be given as an argument to this program.


db = MySQLdb.connect(host='localhost', user='jhm4_john',passwd='skittles',db='jhm4_lab2')
cur = db.cursor()


# This section of code was used to insert test data points into my database

##################################################################################

#address1 = "522 Rosedale Rd, Princeton, NJ 08540"
#address2 = "486 Rosedale Rd, Princeton, NJ 08540"
#address3 = "73 Stockton St, Princeton, NJ 08540"
#address4 =  "282 Mt Lucas Rd, Princeton, NJ 08540"
#address5 = "214 Bayard Ln, Princeton, NJ 08540"

### Since we are assuming a future ability to receive user input from a from we have two approaches:
### 1) We don't immediately assign travelers to certain cars/trips when they sign up and instead
###    wait until 1-3 days before the event when most of the people who are attending have already
###    signed up and then perform a more optimal pairing because we have the full list of attendees.
### 2) We immediately assign users to vehicles/trips when they register, and add them to the currently
###    optimal trip. We won't change this trip once it has been assigned so it may be less than optimal
###    but has the benefit of assigning users immediately.

#geolocator1 = Nominatim()
#geolocator2 = Nominatim()
#geolocator3 = Nominatim()
#geolocator4 = Nominatim()
#geolocator5 = Nominatim()

#location1 = geolocator1.geocode(address1)
#location2 = geolocator2.geocode(address2)
#location3 = geolocator3.geocode(address3)
#location4 = geolocator4.geocode(address4)
#location5 = geolocator5.geocode(address5)

#time = datetime.time(hour=8,minute=00,second=00)
#time2 = datetime.time(hour=7,minute=45,second=00)
#time3 = datetime.time(hour=8,minute=10,second=00)
#time4 = datetime.time(hour=8,minute=00,second=00)
#time5 = datetime.time(hour=8,minute=00,second=00)

#cur.execute("INSERT INTO travelers (fName, lName, event, depTime, oLat, oLon, Hascar, Seats, Email) VALUES ('John 1', 'McDonald', 'Event 1', \'"+str(time)+"\', \'"+ str(location1.latitude) +
#	"\', \'" +str(location1.longitude) +"\', 'Yes', 4, 'jhm41@princeton.edu')")
#cur.execute("INSERT INTO travelers (fName, lName, event, depTime, oLat, oLon, Hascar, Seats, Email) VALUES ('John 2', 'Navarro', 'Event 1', \'"+str(time2)+"\', \'"+ str(location2.latitude) +
#	"\', \'" +str(location2.longitude) +"\', 'No', 0, 'jhm42@princeton.edu')")
#cur.execute("INSERT INTO travelers (fName, lName, event, depTime, oLat, oLon, Hascar, Seats, Email) VALUES ('John 3', 'Martinez', 'Event 1', \'"+str(time3)+"\', \'"+ str(location3.latitude) +
#	"\', \'" +str(location3.longitude) +"\', 'No', 0, 'jhm43@princeton.edu')")
#cur.execute("INSERT INTO travelers (fName, lName, event, depTime, oLat, oLon, Hascar, Seats, Email) VALUES ('Ian', 'Kinn', 'Event 1', \'" + str(time4)+"\', \'"+str(location4.latitude) +
#	"\', \'" +str(location4.longitude) +"\', 'No', 0, 'jhm44@princeton.edu')")
#cur.execute("INSERT INTO travelers (fName, lName, event, depTime, oLat, oLon, Hascar, Seats, Email) VALUES ('Tyler', 'Roth', 'Event 2', \'" + str(time5)+"\', \'"+str(location5.latitude) +
#	"\', \'" +str(location5.longitude) +"\', 'Yes', 0,'jhm45@princeton.edu')")

##################################################################################

###################################################################################
# This is the guts of our website's algorithmic work. Each event would have a date
# associated with it and we would probably use Javascipt to trigger this script
# whenever the event is two or three days away. All this script would need it the
# event name and it could look up the rest of the event information in our events
# database. 
###################################################################################


event = 'Event 1'
eventAddress = "98 Charlton St, Princeton, NJ 08540"
geolocator6 = Nominatim()
destination = geolocator6.geocode(eventAddress)
dLat = destination.latitude
dLon = destination.longitude

destLocation = (dLat, dLon)

# This is a dataframe with all of vehicles for this event. If a user is to be assigned to
# a trip, it will be with one of these users/drivers.
dfCars = pd.read_sql("SELECT * FROM travelers WHERE Hascar='Yes' AND event=\'"+ event+"\'", con=db)

# This is the dataframe with all of our users who need to be paired with a driver.
dfNoCars = pd.read_sql("SELECT * FROM travelers WHERE Hascar='No' AND event=\'"+ event+"\'", con=db)

carsFN = pd.Series(dfCars['fName'])
carsLN = pd.Series(dfCars['lName'])
carsEvent = pd.Series(dfCars['event'])
carsTime = pd.Series(dfCars['depTime'])
carsLat = pd.Series(dfCars['oLat'])
carsLon = pd.Series(dfCars['oLon'])
carsSeats = pd.Series(dfCars['Seats'])
carsEmail = pd.Series(dfCars['Email'])

noneFN = pd.Series(dfNoCars['fName'])
noneLN = pd.Series(dfNoCars['lName'])
noneEvent = pd.Series(dfNoCars['event'])
noneTime = pd.Series(dfNoCars['depTime'])
noneLat = pd.Series(dfNoCars['oLat'])
noneLon = pd.Series(dfNoCars['oLon'])
noneSeats = pd.Series(dfNoCars['Seats'])
noneEmail = pd.Series(dfNoCars['Email'])

# This is just demonstration code. We know that there will only be one vehicle in the
# database that is attending this specific event.
print "With Vehicles:\n"
print carsFN[0] + ", Seats Available: " + str(carsSeats[0])+ "\n "

# We also know that there are only two riders attending this event without vehicles.
print "Without Vehicles:\n"
print noneFN[0] + ", " + noneFN[1] +", " + noneFN[2] + "\n"

length = carsFN.size
vehicleTrips = pd.DataFrame()

i=0
while i <length:
	vehicleTrips=vehicleTrips.append({'Vehicle_Num': str(i+1),'Seats_Avail':carsSeats[i],'OwnerFirstName': carsFN[i],'OwnerLastName':carsLN[i],'Event': carsEvent[i],'depTime':carsTime[i],'oLat':carsLat[i],'oLon':carsLon[i],'Email':carsEmail[i]}, ignore_index=True)
	i=i+1

vNum = pd.Series(vehicleTrips['Vehicle_Num'])
vSeats = pd.Series(vehicleTrips['Seats_Avail'])
vFN = pd.Series(vehicleTrips['OwnerFirstName'])
vLN = pd.Series(vehicleTrips['OwnerLastName'])
vEvent = pd.Series(vehicleTrips['Event'])
vdepTime = pd.Series(vehicleTrips['depTime'])
vLon = pd.Series(vehicleTrips['oLon'])
vLat = pd.Series(vehicleTrips['oLat'])
vEmail = pd.Series(vehicleTrips['Email'])


###################################################################################
# I know that this is currently a suboptimal algorithm. For instance, it doesn't
# keep track of the additional locations so it only checks if a new passenger doesn't
# increase the original trip's length too much vs the current trip. It also doesn't
# allow for people at the new trip stops within a close vicinity to walk to join the
# trip. And it doesn't check permutations of the trip so that additional trips must
# fit within the current trip's structure. But, I have coded these in a previous
# program, but I just wasn't able to fit those in this time because I was stuck on a
# lot of database/server issues that kept me from getting to the algorithmic part of
# this project. We would need to set a maximum number of additional pick up locations
# that a given trip could make in order to extend our algorithm. Then we could
# make space in these dataframe for the locations of these pick up spots and do the 
# necessary permutation calculations to check if additional riders/locations can be
# added to the trip.
###################################################################################
k = 0
vLength = vNum.size
#Iterate through the users with vehicles
while k < vLength:
	seats = vSeats[k]
	thisLat = vLat[k]
	thisLon = vLon[k]

	#Iterate through the users without a car for this trip
	indices = list(noneFN.index)
	for j in indices:
		riderLon = noneLon[j]
		riderLat = noneLat[j]
		riderLocation = (riderLat, riderLon)
		carLocation = (thisLat, thisLon)
		if riderLat< thisLat+.007842/2.0 and riderLat > thisLat-.007842/2 and riderLon <thisLon+.007669/2.0 and riderLon>thisLon-.007669/2.0 and vSeats[k]!=0:
			vSeats[k] = vSeats[k]-1
			vEmail[k] = vEmail[k]+"&"+noneEmail[j]
			noneFN=noneFN.drop([j])
			noneLN=noneLN.drop([j])
			noneEvent=noneEvent.drop([j])
			noneTime=noneTime.drop([j])
			noneLat=noneLat.drop([j])
			noneLon=noneLon.drop([j])
			noneSeats=noneSeats.drop([j])
			noneEmail=noneEmail.drop([j])
		elif (float(vincenty(carLocation,riderLocation).miles)+float(vincenty(riderLocation,destLocation).miles) < 1.25*float(vincenty(carLocation,destLocation).miles)) and vSeats[k]!=0:
			vSeats[k]=vSeats[k]-1
			vEmail[k] = vEmail[k]+"&"+noneEmail[j]
			noneFN=noneFN.drop([j])
			noneLN=noneLN.drop([j])
			noneEvent=noneEvent.drop([j])
			noneTime=noneTime.drop([j])
			noneLat=noneLat.drop([j])
			noneLon=noneLon.drop([j])
			noneSeats=noneSeats.drop([j])
			noneEmail=noneEmail.drop([j])
		if seats==0:
			j=j+1
			break

		j=j+1
	k = k+1

print "Without A Vehicle After:"
print noneFN.head(10)

print vehicleTrips.head(10)



