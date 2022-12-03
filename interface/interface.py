
import python_sdk.strike as strike
import config
import group.group as group
import interface.helper as helper

baseAPI=config.baseAPI

def set_interface_for_new_user(username):
    print(username+" is a New User")
    strikeObj = strike.Create("expenseTrackerBot",baseAPI+"/expenseTrackerBot/register/user?group_id=NA")  
    group_id_question = strikeObj.Question("group_id").\
                QuestionText().\
                SetTextToQuestion("Hi "+username+", please enter a name for your new group?")
    group_id_question.Answer(False).TextInput()

    member_name_question = strikeObj.Question("first_member_name").\
                QuestionText().\
                SetTextToQuestion("What is the name of other memeber?")
    member_name_question.Answer(False).TextInput()
    
    member_number_question = strikeObj.Question("first_member_number").\
                QuestionText().\
                SetTextToQuestion("Enter member's phone number")
    member_number_question.Answer(False).NumberInput()

    return strikeObj

def interface_after_group_created(data,group_id):
    user_name = data["bybrisk_session_variables"]["username"]
    if group_id == "NA":
       group_id = data["user_session_variables"]["group_id"]

    other_memeber_user_name = data["user_session_variables"]["first_member_name"]
        
    strikeObj = strike.Create("expenseTrackerBot",baseAPI+"/expenseTrackerBot/get/action?group_id="+group_id)  
    action_question = strikeObj.Question("action").\
                QuestionText().\
                SetTextToQuestion("Great "+user_name+", I added "+other_memeber_user_name+" to "+group_id+ ". What should I do next?")
    action_answer_card = action_question.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    action_answer_card = action_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"+ Add more member", "#074d69",True)
    action_answer_card = action_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"Add expense to "+group_id, "#074d69",True)
    return strikeObj

def interface_to_add_more_member(data,group_id):
    strikeObj = strike.Create("expenseTrackerBot",baseAPI+"/expenseTrackerBot/register/user?group_id="+group_id)

    member_name_question = strikeObj.Question("first_member_name").\
                QuestionText().\
                SetTextToQuestion("What is the name of other memeber?")
    member_name_question.Answer(False).TextInput()
    
    member_number_question = strikeObj.Question("first_member_number").\
                QuestionText().\
                SetTextToQuestion("Enter member's phone number")
    member_number_question.Answer(False).NumberInput()
    return strikeObj

def set_interface_for_getting_expense_single_group(user_id,group_ids):

    users = group.get_all_user_by_group(group_ids[0][1])
    updater = helper.get_updater(users,user_id)
   
    ## Get the basic interface
    strikeObj = strike.Create("expenseTrackerBot",baseAPI+"/expenseTrackerBot/set/expense?group_id="+group_ids[0][1])  
    strikeObj = basic_interface(strikeObj,updater)       

    if len(users) == 2:
        strikeObj = interface_for_two_people_in_group(strikeObj,updater,users)
    else:    
        strikeObj = interface_for_more_than_two_people_in_group(strikeObj,updater,users)

    return strikeObj        


def basic_interface(strikeObj,updater):
    strikeObj = interface_for_amount_paid(strikeObj,updater) 

    strikeObj = interface_for_category(strikeObj)  

    strikeObj = interface_for_description(strikeObj)
    return strikeObj     

def interface_for_amount_paid(strikeObj,updater):
   amount_paid_question = strikeObj.Question("amount_paid").\
                QuestionText().\
                SetTextToQuestion("Hi "+updater+", enter the amount paid in ₹ ?")
   amount_paid_question.Answer(False).NumberInput()
   return strikeObj

def interface_for_category(strikeObj):
    category_question = strikeObj.Question("category").\
                QuestionText().\
                SetTextToQuestion("Select the category of expense?")
    category_answer_card = category_question.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
    category_answer_card = category_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🍔 Food", "#074d69",True)
    category_answer_card = category_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"💧 Water", "#074d69",True)
    category_answer_card = category_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🛒 Groceries", "#074d69",True)
    category_answer_card = category_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🚌 Transportation", "#074d69",True)
    category_answer_card = category_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🍽️ Dining Out", "#074d69",True)
    category_answer_card = category_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"🏠 Household", "#074d69",True)
    category_answer_card = category_answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"Other", "#074d69",True) 
    return strikeObj                  

def interface_for_description(strikeObj):
    description_question = strikeObj.Question("discription").\
                QuestionText().\
                SetTextToQuestion("What is the expense discription?")
    description_question.Answer(False).TextInput()
    return strikeObj

def interface_for_two_people_in_group(strikeObj,updater,users):
        other_name = helper.get_other_name(users,updater)
        print("[INFO] Updater is "+updater+", Member is "+other_name)

        split_method_question = strikeObj.Question("split_method").\
                QuestionText().\
                SetTextToQuestion("How is the amount paid?")
        answer_card4 = split_method_question.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)
        answer_card4 = answer_card4.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"You paid, split equally", "#3c8c2b",True)
        answer_card4 = answer_card4.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"You are owed the full amount", "#3c8c2b",True)
        answer_card4 = answer_card4.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,other_name+" paid, split equally", "#ad1818",True)
        answer_card4 = answer_card4.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,other_name+" is owed full amount", "#ad1818",True)

        return strikeObj        

def interface_for_more_than_two_people_in_group(strikeObj,updater,users):
        split_method_who_paid_question = strikeObj.Question("split_method_who_paid").\
                QuestionText().\
                SetTextToQuestion("Who paid for this?")
        answer_card4 = split_method_who_paid_question.Answer(False).AnswerCardArray(strike.VERTICAL_ORIENTATION)

        for user in users:
            show_name = user["user_name"]    
            if  show_name == updater:
                show_name = "I"
            answer_card4 = answer_card4.AnswerCard().\
               SetHeaderToAnswer(1,"WRAP").\
               AddTextRowToAnswer(strike.H4,show_name+" paid for this", "#074d69",True)

        split_method_split_among_question = strikeObj.Question("split_method_split_among").\
                QuestionText().\
                SetTextToQuestion("Select which people owe an equal share? long press for multiselect")
        answer_card5 = split_method_split_among_question.Answer(True).AnswerCardArray(strike.VERTICAL_ORIENTATION)

        for user in users:
            show_name = user["user_name"]
            answer_card5 = answer_card5.AnswerCard().\
               SetHeaderToAnswer(1,"WRAP").\
               AddTextRowToAnswer(strike.H4,show_name, "#074d69",True)

        return strikeObj       