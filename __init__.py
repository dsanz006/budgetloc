from flask import Flask, render_template, request, redirect, url_for, abort, session
import json

#GLOBAL VARIABLES
listOfCities = ["copenhagen"]

def calculateItinerary(city, budget, date):
  #_id, name, address, , price, openinghour, closinghour, description, type
  #calculate itinerary here!!!
  it1 = "Museum, Restaurant, Park, Cinema"
  it2 = "Park, Fast Food, Channels, Bar"
  it3 = "Main Square, Restaurant, Museum, Pub"
  it4 = "Museum, Restaurant, Main Square, Night Club"
  itinList = [it1, it2, it3, it4] 
  costList = ["300", "400", "500", "600"]
  print 'calculating...'
  return itinList, costList

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
    try:
      if city.lower() not in listOfCities:
        errorMessage = "Please choose an available city"
        return redirect(url_for('home'))
      else:
        errorMessage = ""
        global itinList
        global costList
        itinList, costList =  calculateItinerary(city, budget, date)
        
        return render_template('summaryPage.html', itin1=itinList[0], itin2=itinList[1], itin3=itinList[2], itin4=itinList[3], 
                                                   cost1=costList[0], cost2=costList[1], cost3=costList[2], cost4=costList[3],
                                                   date=date, city=city, budget=budget)
    except Exception, e:
      return str(e)

@app.route('/anotherPage', methods=['GET'])
def anotherPage():
    try:
      session['chosenButton'] = request.args['itinerary']
    except Exception, e:
      return str(e)
    print 'preferred itinerary is: ', session['chosenButton']
    return redirect(url_for('finalPage'))

@app.route('/finalPage')
def finalPage():
  try:
    city = session['city']
    budget = session['budget']
    date = session['date']
    index = int(session['chosenButton']) - 1
    selectedItinerary = itinList[index]
    selectedCost = costList[index]
    print selectedItinerary, selectedCost
    return render_template('final.html', selectedItinerary=selectedItinerary, selectedCost=selectedCost, 
                                         date=date, city=city, budget=budget)
  except Exception, e:
    return str(e)

if __name__ == '__main__':
    app.run()
