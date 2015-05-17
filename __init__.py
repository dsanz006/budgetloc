from flask import Flask, render_template, request, redirect, url_for, abort, session
import random

#GLOBAL VARIABLES
listOfCities = ["copenhagen"]
kindsOfActivities = ["museum", "amusement park", "castle"]
CALCULATED_ITINERARIES = 3

#We made a hard coded database due to problems to integrate a database with MONGODB and PYTHON in the AMAZON server.
listOfAttractions = [
                {"_id" : 1, "name" : "Amalienborg palace", "address" : "Amalienborg Slotsplats 1", "price" : "70", "openinghour" : "10", "closinghour" : "17", "description" : "Winter Home of the Danish Royal Family", "type" : "museum"}, 
                {"_id" : 2, "name" : "Museum of Copenhagen", "address" : "Uesterbrogade 59", "price" : "40", "openinghour" : "10", "closinghour" : "19", "description" : "Museum of Copenhagen, founded in 1891, documenting the city history from 12th century to the past", "type" : "museum"}, 
                {"_id" : 3, "name" : "The Workers Museum", "address" : "Romersgade22", "price" : "65", "openinghour" : "10", "closinghour" : "16", "description" : "Arbejdermuseet. The museum was opened in 1986", "type" : "museum"}, 
                {"_id" : 4, "name" : "The National Museum", "address" : "Ny Uestergade 10", "price" : "0", "openinghour" : "10", "closinghour" : "17", "description" : "Denmark's largest Museum of cultural history, comprising the histories of danish and foreign cultures", "type" : "museum"}, 
                {"_id" : 5, "name" : "Tivoli Gardens", "address" : "Uesterbrogade 3", "price" : "99", "openinghour" : "11", "closinghour" : "23", "description" : "19th century amusement park", "type" : "amusement park"}, 
                {"_id" : 6, "name" : "Copenhagen Zoo", "address" : "Roskildevej 32", "price" : "170", "openinghour" : "10", "closinghour" : "18", "description" : "Zoological garden in Copenhagen, founded in 1859", "type" : "amusement park"}, 
                {"_id" : 7, "name" : "The Blue Planet", "address" : "Jacob Fortlingsvej 1", "price" : "149", "openinghour" : "10", "closinghour" : "18", "description" : "Huge skeek whirlpool shaped aquarium with fresh and sea water wildlife plus education al displays", "type" : "museum"}, 
                {"_id" : 8, "name" : "Tycho Brahe Planetarium", "address" : "G1 Rongevej 10", "price" : "144", "openinghour" : "10", "closinghour" : "19", "description" : "Named after the astronomer Tycho Brahe, designed by MAA Rnud Munk and opened on November 1989", "type" : "amusement park"}, 
                {"_id" : 9, "name" : "The Round Tower", "address" : "Robmagergade 52", "price" : "25", "openinghour" : "10", "closinghour" : "18", "description" : "The Rundtar is a 17th century tower located in central Copenhagen. It was build as an astronomical observatory", "type" : "castle"}, 
                {"_id" : 10, "name" : "Frederiksberg Palace", "address" : "Montoportvejen 10 34 sO Hillerod", "price" : "75", "openinghour" : "10", "closinghour" : "17", "description" : "Palace in Hillerod. Built as a royal residence for Ring Christian IU and is now a museum of national history", "type" : "castle"}, 
                {"_id" : 11, "name" : "Rosenborg Palace", "address" : "Oster Uolgade 4", "price" : "90", "openinghour" : "10", "closinghour" : "17", "description" : "Rosenborg Castle is a renaissance castle located in Copenhagen. Originally built as a country summerhouse in 1606", "type" : "castle"}
                    ]

#MAIN FUNCTION: ALGORITHM TO CHOOSE POSSIBLE ITINERARIES
def calculateItinerary(city, budget, date):
  #selectedItineraries[]
  #activity{startingTime, endingTime, type, name, description, address, price}
  selectedItineraries = []
  totalPrices = []
  for i in range(CALCULATED_ITINERARIES):
    #EACH ITINERARY
    budgetLeft = int(budget)
    #1ST ACTIVITY: MORNING: 10 T0 13 (or later)
    random.shuffle(kindsOfActivities)
    for activityKind in kindsOfActivities:
      random.shuffle(listOfAttractions)
      for chosenAttraction in listOfAttractions:
        if (chosenAttraction["type"] == activityKind) and (int(chosenAttraction["price"]) <= budgetLeft):
          budgetLeft = budgetLeft - int(chosenAttraction["price"])
          morningActivity = { "startingTime" : max(int(chosenAttraction["openinghour"]),10), "endingTime" : 13 , "type" : activityKind , "name" : chosenAttraction["name"], "description" : chosenAttraction["description"], "address" : chosenAttraction["address"], "price" : chosenAttraction["price"] } 
          break

    #2ND ACTIVITY: AFTERNOON: 15 T0 19 (or earlier)
    random.shuffle(kindsOfActivities)
    for activityKind in kindsOfActivities:
      if activityKind != morningActivity["type"]:
        random.shuffle(listOfAttractions)
        for chosenAttraction in listOfAttractions:
          if (chosenAttraction["type"] == activityKind) and (int(chosenAttraction["price"]) <= budgetLeft) and (int(chosenAttraction["closinghour"]) >= 17):
            budgetLeft = budgetLeft - int(chosenAttraction["price"])
            afternoonActivity = { "startingTime" :  15, "endingTime" : min(int(chosenAttraction["closinghour"]),19), "type" : activityKind , "name" : chosenAttraction["name"], "description" : chosenAttraction["description"], "address" : chosenAttraction["address"], "price" : chosenAttraction["price"] } 
            break

    try:
      afternoonActivity
    except UnboundLocalError:
      afternoonActivity = None

    dayPlan = [morningActivity, afternoonActivity]
    if afternoonActivity == None:
      dayPrice = int(morningActivity["price"])
    else:
      dayPrice = int(morningActivity["price"]) + int(afternoonActivity["price"])
    selectedItineraries.append(dayPlan)
    totalPrices.append(dayPrice)

  return selectedItineraries, totalPrices
          


#WEB SERVER STUFF
app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

@app.route('/')
def home():
  global errorMessage
  try:
    print errorMessage
  except:
    errorMessage = ""
  try:
    return render_template('index.html', errorMessage=errorMessage)
  except Exception, e:
    return str(e)

@app.route('/MainPage', methods=['POST'])
def MainPage():
    session['city'] = request.form['city']
    session['budget'] = request.form['budget']
    session['date'] = request.form['date']
    return redirect(url_for('summary'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/summary')
def summary():
    if not 'city' in session:
        return abort(403)
    
    city = session['city']
    date = session['date']
    budget = session['budget']

    global errorMessage
    try:
      budget = int(budget)
    except Exception, e:
      errorMessage = "Please insert budget correctly"
      return redirect(url_for('home'))

    if city.lower() not in listOfCities:
      errorMessage = "Please choose an available city"
      return redirect(url_for('home'))
    else:
      errorMessage = ""

      global itineraryList
      global totalPriceList

      try:
        itineraryList, totalPriceList = calculateItinerary(city, budget, date)
      except Exception, e:
        return str(e)
      morningList = []
      afternoonList = []
      for itinerary in itineraryList:
        morningAct = itinerary[0]["type"] + " - " + itinerary[0]["name"]
        if itinerary[1] == None:
          afternoonAct = "No budget left!!"
        else:
          afternoonAct = itinerary[1]["type"] + " - " + itinerary[1]["name"]
        morningList.append(morningAct)
        afternoonList.append(afternoonAct)

      return render_template('summaryPage.html', morning1=morningList[0], morning2=morningList[1], morning3=morningList[2], 
                                                 afternoon1=afternoonList[0], afternoon2=afternoonList[1], afternoon3=afternoonList[2], 
                                                 cost1=totalPriceList[0], cost2=totalPriceList[1], cost3=totalPriceList[2],
                                                 date=date, city=city, budget=budget)

@app.route('/anotherPage', methods=['GET'])
def anotherPage():
    session['chosenButton'] = request.args['itinerary']
    chosenIt = session['chosenButton']
    global errorMessage
    try:
      chosenIndex = int(chosenIt)-1
    except:
      errorMessage = "Please choose a valid option"
      return redirect(url_for('home'))

    optionsList = range(CALCULATED_ITINERARIES)
    if chosenIndex not in optionsList:
      errorMessage = "Please choose a valid option"
      return redirect(url_for('home'))
    return redirect(url_for('finalPage'))

@app.route('/finalPage')
def finalPage():
  try:
    city = session['city']
    budget = session['budget']
    date = session['date']
    index = int(session['chosenButton']) - 1
    global itineraryList
    global totalPriceList
    selectedCost = str(totalPriceList[index])
    selectedMorning = itineraryList[index][0]
    if itineraryList[index][1] == None:
      selectedAfternoon = { "startingTime" :  15, "endingTime" : 19, "type" : "None" , "name" : "None", "description" : "None", "address" : "None", "price" : 0 } 
    else:
      selectedAfternoon = itineraryList[index][1]

    return render_template('final.html', selectedCost=selectedCost, city=city, date=date, budget=budget,
                                         start1=str(selectedMorning["startingTime"]), end1=str(selectedMorning["endingTime"]), name1=selectedMorning["name"], type1=selectedMorning["type"], description1=selectedMorning["description"], address1=selectedMorning["address"], price1=str(selectedMorning["price"]), 
                                         start2=str(selectedAfternoon["startingTime"]), end2=str(selectedAfternoon["endingTime"]), name2=selectedAfternoon["name"], type2=selectedAfternoon["type"], description2=selectedAfternoon["description"], address2=selectedAfternoon["address"], price2=str(selectedAfternoon["price"]))
  except Exception, e:
    return str(e)

if __name__ == '__main__':
    app.run()
