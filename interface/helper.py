import sql
import group.group as group
import interface.interface as interface

def get_updater(users,user_id):
    for user in users:
        if user["user_id"] == user_id:
           return user["user_name"]

def get_other_name(users,updater):
    for user in users:
        if user["user_name"] != updater:
            return user["user_name"]

def insert_first_member(data,group_id):
    user_id = data["bybrisk_session_variables"]["userId"]
    user_name = data["bybrisk_session_variables"]["username"]
    user_phone = data["bybrisk_session_variables"]["phone"]
    other_memeber_user_name = data["user_session_variables"]["first_member_name"]
    other_memeber_phone = data["user_session_variables"]["first_member_number"]
    if group_id == "NA":
      group_id = data["user_session_variables"]["group_id"]  
      sql.register_user(group_id,user_phone,user_name)
      sql.register_user(group_id,other_memeber_phone,other_memeber_user_name)                
    else:
      sql.register_user(group_id,other_memeber_phone,other_memeber_user_name)  

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