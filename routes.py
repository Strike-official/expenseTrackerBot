import python_sdk.strike as strike #For timebeing, strike is a private library. Has to be downloaded into the local from https://github.com/Strike-official/python-sdk 
import config
import flask
import requests
from flask import jsonify
from flask import request
import sql
import group
import interface 

app = flask.Flask(__name__)
app.config["DEBUG"] = True


baseAPI=config.baseAPI

@app.route('/expenseTrackerBot/get/expense', methods=['POST'])
def get_location_for_booking():

    data = request.get_json()
    user_id = data["bybrisk_session_variables"]["userId"]
    strikeObj = strike.Create("expenseTrackerBot",baseAPI)

    ## Get active group
    user_state,group_ids = group.get_all_group(user_id)

    if user_state == "NEW":
        ## Let user create a group
    if user_state == "SINGLE_GROUP":
        ## Select the only group user have
        strikeObj = interface.set_interface_for_getting_expense()
    if user_state == "MULTI_GROUP":
        ## Let user select the group      
    
    return jsonify(strikeObj.Data())

@app.route('/expenseTrackerBot/set/expense', methods=['POST'])
def respondBack():
    data = request.get_json()
    print(data)
    user_id = data["bybrisk_session_variables"]["userId"]
    amount_paid = data["user_session_variables"]["amount_paid"]
    userName = data["bybrisk_session_variables"]["username"]
    
    category = data["user_session_variables"]["category"][0]
    categoryPlain = "Other"
    if category != "Other":
        categoryArr = category.split(" ")
        categoryPlain = categoryArr[1]
    
    discription = data["user_session_variables"]["discription"]
    split_method = data["user_session_variables"]["split_method"][0]


    ## Save to DB
    sql.add_expense(user_id,"FOUNDER",amount_paid,categoryPlain,discription,split_method)

    text,color = compute_balence(user_id,userName)

    strikeObj = strike.Create("foodTrackBot","")
    question_card = strikeObj.Question("").\
            QuestionCard().\
            SetHeaderToQuestion(11,strike.HALF_WIDTH).\
            AddGraphicRowToQuestion(strike.PICTURE_ROW,["https://media.istockphoto.com/id/474551486/photo/3d-white-man-with-green-tick.jpg?s=612x612&w=0&k=20&c=aiPfi5CiH8Ru4jGy29Z4O_X9rDrykS5CanfoWtt0dRI="],[""]).\
            AddTextRowToQuestion(strike.H4,"This expense has been added","#074d69",False).\
            AddTextRowToQuestion(strike.H4,text,color,True)

    return jsonify(strikeObj.Data())        


@app.route('/expenseTrackerBot/get/distribution', methods=['POST'])
def getDistribution():
    data = request.get_json()
    user_id = data["bybrisk_session_variables"]["userId"]
    userName = data["bybrisk_session_variables"]["username"]

    text,color = compute_balence(user_id,userName)                  

    strikeObj = strike.Create("foodTrackBot","")
    question_card = strikeObj.Question("").\
            QuestionCard().\
            SetHeaderToQuestion(11,strike.HALF_WIDTH).\
            AddTextRowToQuestion(strike.H4,text,color,False)           

    return jsonify(strikeObj.Data())

def not_user(users,username):
   for user in users:
     if user!=username:
        return user

def compute_balence(user_id,userName):
    you_get = 0    
    ## Get data from DB
    expense_results = sql.get_expense("FOUNDER")
    for expense_result in expense_results:
      if expense_result[6] == "You paid, split equally":
         if expense_result[1] == user_id:
           you_get = you_get + (expense_result[3]/2)
         else:
           you_get = you_get + (-1*(expense_result[3]/2))
      if expense_result[6] == "You are owed the full amount":
         if expense_result[1] == user_id:
           you_get = you_get + (expense_result[3])
         else:
           you_get = you_get + (-1*(expense_result[3]))  
      for user in ["Sayak","Shashank"]:
        if expense_result[6] == user+" paid, split equally":
            if expense_result[1] == user_id:
                you_get = you_get + (-1*(expense_result[3]/2))
        if expense_result[6] == user+" is owed full amount":
            if expense_result[1] == user_id:
                you_get = you_get + (-1*expense_result[3])

    users = ["Sayak","Shashank"]
    if you_get > 0:
        text = not_user(users,userName)+" owes you ₹"+str(you_get)
        color =  "#3c8c2b"
    if you_get < 0:
        text = "You owe "+not_user(users,userName)+" ₹"+str((-1*you_get))
        color =  "#ad1818"
    if you_get == 0:
        text = "Things are settled up. You owe nothing to "+not_user(users,userName)
        color =  "#3c8c2b"    
    return text,color                              

app.run(host='0.0.0.0', port=config.port) 