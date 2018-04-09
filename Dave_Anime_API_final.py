import requests
from bs4 import BeautifulSoup

def getShows(username):
	#DECLARING STUFF
	showsWatched = []
	planList = []
	watchedCode = "2"
	planCode = "6"
	#GET DATA
	call = "https://myanimelist.net/malappinfo.php?u=" + username + "&status=all&type=anime"
	response = requests.get(call)
	#PARSE DATA	
	soup = BeautifulSoup(response.text, "xml")
	shows = soup.find_all('series_title')
	watchStatus = soup.find_all('my_status')
	#FORMAT DATA
	for x in range(0, len(shows)):
		shows[x] = shows[x].text
		watchStatus[x] = watchStatus[x].text
	#SEPERATE DATA INTO TWO LISTS WATCHED AND PLAN TO WATCH
	for x in range(0,len(shows)):
		if watchStatus[x] == watchedCode:
			showsWatched.append(shows[x])
		elif watchStatus[x] == planCode:
			planList.append(shows[x])
	#SORT LISTS INTO ALPHABETICAL ORDER 
	showsWatched.sort()
	planList.sort()
	#RETURN DATA
	tempDict  = dict(name=username,watched=showsWatched,plan=planList,safePlan = [])
	return tempDict
	
def getWatch():
#PROMPT USER FOR USERNAME TO LOOK UP
	user = input("\nEnter the user you would like to see the watchlist of\n")
	print("\n")
#FIND USER
	for x in range(0,numUser):
		if dictList[x]['name'] == user:
#PRINT THE WATCH LIST
			for y in range(0,len(dictList[x]['watched'])):
				print(dictList[x]['watched'][y])

def getPlan():
#FIND USER
	user = input("\nEnter the user you would like to see the watchlist of\n")
	print("\n")
	for x in range(0,numUser):
		if dictList[x]['name'] == user:
#PRINT PLAN LIST
			for y in range(0,len(dictList[x]['plan'])):
				print(dictList[x]['plan'][y])

def getWatchPlan():
#FIND USER
	user = input("\nEnter the user you would like to see the watchlist of\n")
	print("\n")
	for x in range(0,numUser):
		if dictList[x]['name'] == user:
#PRINT WATCH LIST
				print("Watch List\n")
				for y in range(0,len(dictList[x]['watched'])):
					print(dictList[x]['watched'][y])
#PRINT PLAN LIST
				print("\nPlan List\n")
				for y in range(0,len(dictList[x]['plan'])):
					print(dictList[x]['plan'][y])

def showWatch():
	print("\n")
#PRINT THE NO NO LIST
	for x in range(0,len(noNoList)):
		print(noNoList[x])

def countFinal():
	print("\n")
#CREATE LIST THAT WILL HOLD 1 OF EACH ITEM FROM COMBINED LIST
	shortCombined = []
#SORT THE COMBINED LIST BY THE AMOUNT OF APPEARENCES OF AN ITEM IN THE LIST HIGHEST FIRST
	sortedCombined = sorted(combinedList, key=combinedList.count, reverse=True)
#INSERT ITEMS INTO SHORT COMBINED LIST
	for x in range(0,len(sortedCombined)):
		if sortedCombined[x] in shortCombined:	
			pass
		else:
			shortCombined.append(sortedCombined[x])
#OUTPUT FORMATTED INFO
	for x in range(0,len(shortCombined)):
		print("%-65s %5d" %(shortCombined[x], sortedCombined.count(shortCombined[x])))

def getAllWatchPlan():
#OUTPUT THE USERNAME, WATCHED SHOWS, AND PLAN LIST OF EACH DICT
	for x in range(0,numUser):
		print("\nUSERNAME " + dictList[x]['name'] + "\n")
		print("WATCHED SHOWS \n")
		for y in range(0,len(dictList[x]['watched'])):
					print(dictList[x]['watched'][y])
		print("\nPLAN LIST\n")
		for y in range(0,len(dictList[x]['plan'])):
					print(dictList[x]['plan'][y])
	
def exit():
#EXIT PROGRAM
	quit()

#######MAIN PROGRAM##############
#DECLARE LISTS
dictList = []
noNoList = []
combinedList = []
finalList = []
#PROMPT FOR USER INPUT
numUser = int(input("What is the number of users\n"))
#MAKE THE LIST OF SHOWS THAT SHOULDNT BE WATCHED
for x in range (0, numUser):
	name = input("Enter a User Name ")
	dictList.append(getShows(name))
	for y in range(0,len(dictList[x]['watched'])):
		if dictList[x]['watched'][y] in noNoList:
			pass
		else:
			noNoList.append(dictList[x]['watched'][y])	
#SORT THE SHOWS WATCHED LIST
noNoList.sort() 
#RUN THROUGH WATCH LISTS TO SEE WHAT PLAN TO WATCH ARE NOT IN WATCHED ALREADY
for x in range (0, numUser):
	for y in range(0,len(dictList[x]['plan'])):
		if dictList[x]['plan'][y] in noNoList:
			pass
		else:
			dictList[x]['safePlan'].append(dictList[x]['plan'][y])
#MOVE ALL SHOWS FROM EVERY USERS SAFE WATCH LIST INTO A SINGLE LIST
	for y in range(0,len(dictList[x]['safePlan'])):
		combinedList.append(dictList[x]['safePlan'][y])
#ASSEMBLE THE FINAL LIST
for x in range (0,len(combinedList)):
	if combinedList.count(combinedList[x]) == numUser:
		if combinedList[x] in finalList:
			pass
		else:
			finalList.append(combinedList[x])
#LOOP TO DO MORE STUFF IF USER WANTS
while(1):
#PRINT OUT THE SHOWS THAT ARE ON EVERY USERS PLAN TO WATCH LIST
	print("\nThe shows that are on each user's plan to watch list that no user has watched are")
	print(finalList) 
#PROMPT USER FOR NEXT STEP
	whatNext = int(input("\nEnter the number of the next step.\n1) Get a person's watched list.\n2) \
Get a persons plan to watch list.\n3) Get a persons watched and plan to watch lists.\n4)\
 Show the sorted combined watch list.\n5) Count the amount of users that had each show on thier watch list.\n\
6) Show ALL users watched and plan to watch lists.\n7) \
End\n"))
#MAKE A SWITCH STATEMENT OUT OF A DICT CUZ PYTHON REASONS
	fakeSwitch = switcher = {
		1: getWatch,
		2: getPlan,
		3: getWatchPlan,
		4: showWatch,
		5: countFinal,
		6: getAllWatchPlan,
		7: exit,
	}
#ENSURE IT WAS A PROPER INPUT THEN CALL THE FUNCTION USER REQUESTED
	if whatNext > 0 and whatNext < 8:
		fakeSwitch[whatNext]()
	else:
		print("Invalid Option")


