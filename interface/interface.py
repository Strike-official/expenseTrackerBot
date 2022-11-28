
import python_sdk.strike as strike
import config

baseAPI=config.baseAPI

def set_interface_for_getting_expense():
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

    return strikeObj        