import sql
import group.group as group
import interface.interface as interface

expense_updated_for_group = {}
ledger_for_group = {}

group_map = {
    "6392e3b6040e6322f17cbb7f":"SM Silver Oak",
    "623e12d995ba637fe92fb079":"SM Silver Oak",
    "623efb9195ba637fe92fb07b":"SM Silver Oak"
}

users_id_map = {
        "Shashi":"6392e3b6040e6322f17cbb7f",
        "Sayak":"623e12d995ba637fe92fb079",
        "Shashank":"623efb9195ba637fe92fb07b"
}

def get_updater(users,user_id):
    for user in users:
        if user["user_id"] == user_id:
           return user["user_name"]

def get_other_name(users,updater):
    for user in users:
        if user["user_name"] != updater:
            return user["user_name"]

def insert_first_member(data,group_name):
    user_id = data["bybrisk_session_variables"]["userId"]
    user_name = data["bybrisk_session_variables"]["username"]
    user_phone = data["bybrisk_session_variables"]["phone"]
    other_memeber_user_name = data["user_session_variables"]["first_member_name"]
    other_memeber_phone = data["user_session_variables"]["first_member_number"]
    if group_name == "NA":
      group_name = data["user_session_variables"]["group_name"]  
      sql.register_user(group_name,user_phone,user_name)
      sql.register_user(group_name,other_memeber_phone,other_memeber_user_name)                
    else:
      sql.register_user(group_name,other_memeber_phone,other_memeber_user_name)  

def get_group_and_set_expense(user_id_phone,username):
    user_state,group_ids = group.get_all_group(user_id_phone)

    if user_state == "NEW":
        strikeObj = interface.set_interface_for_new_user(username)
    if user_state == "SINGLE_GROUP":
        strikeObj = interface.set_interface_for_getting_expense_single_group(user_id_phone,group_ids)
    if user_state == "MULTI_GROUP":
        ## Let user select the group
        print("user has multi group")    
    return strikeObj   

def get_among_who_string_literal(data):
    split_method_split_among = data["user_session_variables"]["split_method_split_among"]
    split_method_split_among_str = ""
    for i in split_method_split_among:
        split_method_split_among_str = i + "|" +split_method_split_among_str 
    return  split_method_split_among_str  

def get_who_paid_string_litral(data,userName):
    split_method_who_paid_raw = data["user_session_variables"]["split_method_who_paid"][0]
    split_method_who_paid_arr = split_method_who_paid_raw.split(" paid for ")
    split_method_who_paid = split_method_who_paid_arr[0]
    if split_method_who_paid == "I":
        split_method_who_paid = userName            
    return split_method_who_paid

def getTargetUsersForGroup(group_id, split_among, current_user_id):
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
 

def getUserFromName(name):
    return users_id_map[name]

def getUserNameFromId(uid):
    for k in users_id_map:
        if users_id_map[k]==uid:
            return k

def addToTransactionLedger(expense_id, group_id, who_paid, for_whom_id_list, amount):
    print("########################################")
    print(expense_id, group_id, who_paid, for_whom_id_list, amount)
    print("\n")
    for_whom_array = for_whom_id_list.split("|")[:-1]
    # print(for_whom_array)
    individual_amount = round((int(amount)/len(for_whom_array)),2)
    who_paid_id = getUserFromName(who_paid)
    for w in for_whom_array:
        for_whom_id = getUserFromName(w)
        # print(expense_id, group_id, who_paid_id, for_whom_id, individual_amount)
        sql.add_expense_to_ledger(expense_id, group_id, who_paid_id, for_whom_id, individual_amount)
        if who_paid_id != for_whom_id:
            if ledger_for_group.get(group_id) == None: ledger_for_group[group_id] = {}
            if ledger_for_group[group_id].get(who_paid_id) == None: ledger_for_group[group_id][who_paid_id] = {}
            if ledger_for_group[group_id][who_paid_id].get(for_whom_id) == None: ledger_for_group[group_id][who_paid_id][for_whom_id] = 0
            ledger_for_group[group_id][who_paid_id][for_whom_id] += individual_amount
            
            if ledger_for_group.get(group_id) == None: ledger_for_group[group_id] = {}
            if ledger_for_group[group_id].get(for_whom_id) == None: ledger_for_group[group_id][for_whom_id] = {}
            if ledger_for_group[group_id][for_whom_id].get(who_paid_id) == None: ledger_for_group[group_id][for_whom_id][who_paid_id] = 0
            ledger_for_group[group_id][for_whom_id][who_paid_id] += -1*individual_amount
    # print(ledger_for_group) 
    return None

def populateInMemLedger():
    data = sql.get_expense_from_ledger()
    print("Populating In-mem Ledger")
    for d in data:
        group_id,who_paid_id,for_whom_id,amount = d[0],d[1],d[2],d[3]
        if who_paid_id == for_whom_id: continue
        
        if ledger_for_group.get(group_id) == None: ledger_for_group[group_id] = {}
        if ledger_for_group[group_id].get(who_paid_id) == None: ledger_for_group[group_id][who_paid_id] = {}
        if ledger_for_group[group_id][who_paid_id].get(for_whom_id) == None: 
            ledger_for_group[group_id][who_paid_id][for_whom_id] = amount
        else:
            ledger_for_group[group_id][who_paid_id][for_whom_id] += amount

        # Inverse of above
        group_id,for_whom_id,who_paid_id,amount = d[0],d[1],d[2],(-1*d[3])
        if ledger_for_group.get(group_id) == None: ledger_for_group[group_id] = {}
        if ledger_for_group[group_id].get(who_paid_id) == None: ledger_for_group[group_id][who_paid_id] = {}
        if ledger_for_group[group_id][who_paid_id].get(for_whom_id) == None: 
            ledger_for_group[group_id][who_paid_id][for_whom_id] = amount
        else:
            ledger_for_group[group_id][who_paid_id][for_whom_id] += amount


def getGroupForUid(uid):
    return group_map[uid]

# TODO
def populateGroupForUid():
    print("---- TODO populateGroupForUid")
    # data = sql.get_all_expense_group()
    # for d in data:
    #     uid,grpid = d[0],d[1]
    #     group_map[uid] = grpid

    return None

def setGroupForUid(uid,grp):
    group_map[uid]=grp

def compute_ledger_balence(uid):
    group_id = getGroupForUid(uid)
    # print("compute_ledger_balence "+group_id)
    if ledger_for_group.get(group_id) == None: return ["No data found in the group"], ["black"]
    if ledger_for_group[group_id].get(uid) == None: return ["Users not found in the group"], ["black"]
    # print(ledger_for_group[group_id][uid])
    txt = []
    color = []
    final_value = 0
    for key in ledger_for_group[group_id][uid]:
        value = ledger_for_group[group_id][uid][key]
        final_value += value
        if value < 0:
            text = "You owe "+getUserNameFromId(key)+" ₹"+str(-1*value)
            clr = "#ad1818"
        elif value==0:
            text = "You are all settled with "+getUserNameFromId(key)
            clr = "#28231D"
        else:
            text = getUserNameFromId(key)+" owes you ₹"+str(value)
            clr = "#3c8c2b"
        txt.append(text)
        color.append(clr)
    finalTxt = []
    finalColor = []
    if final_value < 0:
        text = "You owe ₹"+str(-1*final_value)
        clr = "#ad1818"
    elif value==0:
        text = "You are all Clear!"
        clr = "#28231D"
    else:
        text = "You are owed ₹"+str(final_value)
        clr = "#3c8c2b"

    finalTxt.append(text)
    finalColor.append(clr)
    for t in txt: finalTxt.append(t)
    for c in color: finalColor.append(c)

    return finalTxt,finalColor

def populateLedgerFromOlderData():
    data = sql.tempSql()
    for d in data:
        group_id, amount, who_paid,to_whom_str,expense_id = d[0],d[1],d[2],d[3],d[4]
        to_whom_arr = to_whom_str.split("|")[:-1]
        individual_amount = round((int(amount)/len(to_whom_arr)),2)
        who_paid_id = getUserFromName(who_paid)
        for w in to_whom_arr:
            to_whom_id = getUserFromName(w)
            print(expense_id, group_id, who_paid_id, to_whom_id, individual_amount)
            # sql.add_expense_to_ledger(expense_id, group_id, who_paid_id, to_whom_id, individual_amount)

