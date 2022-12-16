import python_sdk.strike as strike #For timebeing, strike is a private library. Has to be downloaded into the local from https://github.com/Strike-official/python-sdk 
import config
import flask
import requests
from flask import jsonify
from flask import request
import sql
import notification
import group.group as group
import interface.interface as interface
import interface.helper as helper

app = flask.Flask(__name__)
app.config["DEBUG"] = True


baseAPI=config.baseAPI

@app.route('/expenseTrackerBot/get/expense', methods=['POST'])
def get_expense():

    data = request.get_json()
    user_id = data["bybrisk_session_variables"]["phone"]
    username = data["bybrisk_session_variables"]["username"]
    strikeObj = strike.Create("expenseTrackerBot",baseAPI)

    strikeObj = helper.get_group_and_set_expense(user_id,username)
    
    return jsonify(strikeObj.Data())

@app.route('/expenseTrackerBot/set/expense', methods=['POST'])
def respondBack():
    data = request.get_json()
    print(data)
    user_id = data["bybrisk_session_variables"]["userId"]
    app_id = data["bybrisk_session_variables"]["businessId"]
    amount_paid = data["user_session_variables"]["amount_paid"]
    userName = data["bybrisk_session_variables"]["username"]
    group_id = request.args.get('group_id')
    
    category = data["user_session_variables"]["category"][0]
    categoryPlain = "Other"
    if category != "Other":
        categoryArr = category.split(" ")
        categoryPlain = categoryArr[1]
    
    discription = data["user_session_variables"]["discription"]
    
    if "split_method" in data["user_session_variables"].keys():
        split_method = data["user_session_variables"]["split_method"][0]
        sql.add_expense(user_id,group_id,amount_paid,categoryPlain,discription,split_method,"NA","NA")
    else:
        split_method_who_paid = helper.get_who_paid_string_litral(data,userName)
        split_method_split_among_str = helper.get_among_who_string_literal(data)  
        sql.add_expense(user_id,group_id,amount_paid,categoryPlain,discription,"GROUP",split_method_who_paid,split_method_split_among_str)
        notification_text = userName+" added ₹"+amount_paid+" for "+discription+"\nSplitted-Among: "+split_method_split_among_str+"\nPaid-By:"+split_method_who_paid
        users = getUsersForGroup(group_id, split_method_split_among_str, user_id)
        for uid in users:
            notification.push(uid, app_id, notification_text)
    ## Save to DB
    

    ##text,color = compute_balence(user_id,userName)

    strikeObj = strike.Create("foodTrackBot",baseAPI+"/expenseTrackerBot/get/action?group_id="+group_id)
    question_card = strikeObj.Question("action").\
            QuestionCard().\
            SetHeaderToQuestion(11,strike.HALF_WIDTH).\
            AddGraphicRowToQuestion(strike.PICTURE_ROW,["https://media.istockphoto.com/id/474551486/photo/3d-white-man-with-green-tick.jpg?s=612x612&w=0&k=20&c=aiPfi5CiH8Ru4jGy29Z4O_X9rDrykS5CanfoWtt0dRI="],[""]).\
            AddTextRowToQuestion(strike.H4,"I added the expense to "+group_id,"#074d69",False)
            ##AddTextRowToQuestion(strike.H4,text,color,True)
    action_answer_card = question_card.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    action_answer_card = action_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"+ Add more member", "#074d69",True)
    action_answer_card = action_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"Add expense to "+group_id, "#074d69",True)        

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

@app.route('/expenseTrackerBot/register/user', methods=['POST'])
def register_user():
    data = request.get_json()
    group_id = request.args.get('group_id')
    helper.insert_first_member(data,group_id)
    strikeObj = interface.interface_after_group_created(data,group_id)
    return jsonify(strikeObj.Data())

@app.route('/expenseTrackerBot/get/action', methods=['POST'])
def get_action():
    data = request.get_json()
    action = data["user_session_variables"]["action"][0]
    print(action)
    group_id = request.args.get('group_id')
    strikeObj = strike.Create("expenseTrackerBot",baseAPI)

    if action == "+ Add more member":
        strikeObj = interface.interface_to_add_more_member(data,group_id)
    if action == ("Add expense to "+group_id):
        user_id = data["bybrisk_session_variables"]["phone"]
        username = data["bybrisk_session_variables"]["username"]
        strikeObj = helper.get_group_and_set_expense(user_id,username)

    return jsonify(strikeObj.Data())

def getUsersForGroup(group_id, split_among, current_user_id):
    split_among_users = split_among.split("|")
    users = {
        "Shashi":"6392e3b6040e6322f17cbb7f",
        "Sayak":"623e12d995ba637fe92fb079",
        "Shashank":"623efb9195ba637fe92fb07b"
    }
    targetUsers = []
    for u in users:
        if u in split_among_users and users[u] != current_user_id:
            targetUsers.append(users[u])
    return targetUsers

app.run(host='0.0.0.0', port=config.port) 