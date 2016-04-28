from flask import Flask
from flask import render_template
from flask import request, redirect

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

from twilio.rest import TwilioRestClient

###

def get_menu():
    menu_url = "https://aspc.pomona.edu/menu/"
    response = requests.get(menu_url) #html from aspc website
    
    if response.status_code == 404:                 
        print("There was a problem with getting the page:")
        print(menu_url)
        
    data_from_url = response.text  # convert to text
    soup = BeautifulSoup(data_from_url, "html.parser") #convert to beautiful soup
    
    global L #list of all items that fall withing the tag li
    L = []
    Frank_dict=defaultdict(list)
    Frary_dict=defaultdict(list)
    Oldenborg_dict=defaultdict(list)
    CMC_dict=defaultdict(list)
    Scripps_dict=defaultdict(list)
    Pitzer_dict=defaultdict(list)
    Mudd_dict=defaultdict(list)
    Final_dict=defaultdict(dict)

    TRL = soup.findAll('tr')

    #Frank
    TDL = TRL[3].findAll('td')
    for tag in TDL: #Meal times
        meal=tag.findAll('span')
        first_meal=meal[0]
        mealstr=first_meal.next_element
        LIL=tag.findAll("li")
        menu_list=[]
        for item in LIL: #food items
            menu_items = item.next_element
            menu_items_str = str(menu_items)
            menu_list+=[menu_items]
        Frank_dict[mealstr]+=menu_list

    #Frary
    TDL = TRL[4].findAll('td')
    for tag in TDL: #Meal times
        meal=tag.findAll('span')
        first_meal=meal[0]
        mealstr=first_meal.next_element
        LIL=tag.findAll("li")
        menu_list=[]
        for item in LIL: #food items
            menu_items = item.next_element
            menu_items_str = str(menu_items)
            menu_list+=[menu_items]
        Frary_dict[mealstr]+=menu_list

    #Oldenborg
    TDL = TRL[5].findAll('td')
    for tag in TDL: #Meal times
        meal=tag.findAll('span')
        first_meal=meal[0]
        mealstr=first_meal.next_element
        LIL=tag.findAll("li")
        menu_list=[]
        for item in LIL: #food items
            menu_items = item.next_element
            menu_items_str = str(menu_items)
            menu_list+=[menu_items]
        Oldenborg_dict[mealstr]+=menu_list

    #CMC
    TDL = TRL[6].findAll('td')
    for tag in TDL: #Meal times
        meal=tag.findAll('span')
        first_meal=meal[0]
        mealstr=first_meal.next_element
        LIL=tag.findAll("li")
        menu_list=[]
        for item in LIL: #food items
            menu_items = item.next_element
            menu_items_str = str(menu_items)
            menu_list+=[menu_items]
        CMC_dict[mealstr]+=menu_list

    #Scripps
    TDL = TRL[7].findAll('td')
    for tag in TDL: #Meal times
        meal=tag.findAll('span')
        first_meal=meal[0]
        mealstr=first_meal.next_element
        LIL=tag.findAll("li")
        menu_list=[]
        for item in LIL: #food items
            menu_items = item.next_element
            menu_items_str = str(menu_items)
            menu_list+=[menu_items]
        Scripps_dict[mealstr]+=menu_list

    #Pitzer
    TDL = TRL[8].findAll('td')
    for tag in TDL: #Meal times
        meal=tag.findAll('span')
        first_meal=meal[0]
        mealstr=first_meal.next_element
        LIL=tag.findAll("li")
        menu_list=[]
        for item in LIL: #food items
            menu_items = item.next_element
            menu_items_str = str(menu_items)
            menu_list+=[menu_items]
        Pitzer_dict[mealstr]+=menu_list

    #Mudd
    TDL = TRL[9].findAll('td')
    for tag in TDL: #Meal times
        meal=tag.findAll('span')
        first_meal=meal[0]
        mealstr=first_meal.next_element
        LIL=tag.findAll("li")
        menu_list=[]
        for item in LIL: #food items
            menu_items = item.next_element
            menu_items_str = str(menu_items)
            menu_list+=[menu_items]
        Mudd_dict[mealstr]+=menu_list
    L=[Frank_dict]+[Frary_dict]+[Oldenborg_dict]+[CMC_dict]+[Scripps_dict]+[Pitzer_dict]+[Mudd_dict]
    return(L)


def match_food(item):
    L=get_menu()
    halls=['Frank', 'Frary', 'Oldenborg', 'CMC', 'Scripps', 'Pitzer', 'Mudd']
    Matchstr=''
    for i in range(len(L)):
        for x in item:
            match_list=process.extract(x, L[i]['Breakfast'], limit=1)
            score=match_list[0][1]
            if score>80:
                Matchstr+= str(halls[i])+' has '+str(match_list[0][0])+' for breakfast, '

            match_list=process.extract(x, L[i]['Lunch'], limit=1)
            score=match_list[0][1]
            if score>80:
                Matchstr+= str(halls[i])+' has '+str(match_list[0][0])+' for lunch, '

            match_list=process.extract(x, L[i]['Dinner'], limit=1)
            score=match_list[0][1]
            if score>80:
                Matchstr+= str(halls[i])+' has '+str(match_list[0][0])+' for dinner, '
    Finalstr=Matchstr[:-2]+'.'
    return Finalstr

###

# Twilio API
ACCOUNT_SID = 'AC9629dc758c9d995440c7b90b5542d86c'
AUTH_TOKEN =  'b13ff78cc4235ddbabcf41decd4269ee'

# Flask app
app = Flask(__name__)
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# Twilio number
twilio_number = "+17797747983" 

# App exectution 
@app.route("/") 
def main():
    return render_template('form.html')

# Receiver's number and app outgoing message 
@app.route("/submit-form/", methods = ['POST'])
def submit_number():
    global food 
    food = request.form['food']
    print(food)
    global formatted_food
    formatted_food = str(food)
    global pattern
    pattern = re.compile("^\s+|\s*,\s*|\s+$")
    global food_list
    food_list=[x for x in pattern.split(formatted_food) if x]
    global food_input
    food_input = match_food(food_list)
    print(food_input)
    short_food_input=food_input[:160]
    #print(food)
    #print(formatted_food)
    #print(food_input)
    #global number
    number = request.form['number']
    #global formatted_number
    formatted_number = "+1" + number 
    print(formatted_number)
    print(twilio_number)
    # changed from client.sms.messages.create
    client.messages.create(to=formatted_number, from_ = twilio_number,
     body = food_input) 
    return redirect('/messages/')
    
# Incoming messages 
@app.route("/messages/")
def list_messages():
    return render_template('messages.html')

# Command line exexution 
if __name__ == '__main__': 
    app.run('0.0.0.0', port = 3000, debug = False)





