import python_sdk.strike as strike #For timebeing, strike is a private library. Has to be downloaded into the local from https://github.com/Strike-official/python-sdk 
import config
import flask
import requests
from flask import jsonify
from flask import request
import sql

app = flask.Flask(__name__)
app.config["DEBUG"] = True


baseAPI=config.baseAPI

@app.route('/expenseTrackerBot/get/expense', methods=['POST'])
def get_location_for_booking():

    data = request.get_json()
    user_id = data["bybrisk_session_variables"]["userId"]

    if user_id == "623efb9195ba637fe92fb07b":
        otherName = "Sayak"
    else: 
        otherName = "Shashank"
    
    
    
    strikeObj = strike.Create("expenseTrackerBot",baseAPI+"/expenseTrackerBot/set/expense")

    quesObj3 = strikeObj.Question("amount_paid").\
                QuestionText().\
                SetTextToQuestion("Enter the amount in ₹ ?")
    quesObj3.Answer(False).NumberInput()

    quesObj2 = strikeObj.Question("category").\
                QuestionText().\
                SetTextToQuestion("What is the category of expense?")
    answer_card2 = quesObj2.Answer(False).AnswerCardArray(strike.HORIZONTAL_ORIENTATION)
    answer_card2 = answer_card2.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🍔 Food", "#074d69",True)
    answer_card2 = answer_card2.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"💧 Water", "#074d69",True)
    answer_card2 = answer_card2.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🛒 Groceries", "#074d69",True)
    answer_card2 = answer_card2.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🚌 Transportation", "#074d69",True)
    answer_card2 = answer_card2.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🍽️ Dining Out", "#074d69",True)
    answer_card2 = answer_card2.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🏠 Household", "#074d69",True)
    answer_card2 = answer_card2.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"Other", "#074d69",True)  

    quesObj1 = strikeObj.Question("discription").\
                QuestionText().\
                SetTextToQuestion("What is the expense discription?")
    quesObj1.Answer(False).TextInput()                                  

    quesObj4 = strikeObj.Question("split_method").\
                QuestionText().\
                SetTextToQuestion("How is the amount paid?")
    answer_card4 = quesObj4.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    answer_card4 = answer_card4.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"You paid, split equally", "#3c8c2b",True)
    answer_card4 = answer_card4.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"You are owed the full amount", "#3c8c2b",True)
    answer_card4 = answer_card4.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,otherName+" paid, split equally", "#ad1818",True)
    answer_card4 = answer_card4.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,otherName+" is owed full amount", "#ad1818",True)
    
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