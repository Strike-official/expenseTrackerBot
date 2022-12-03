import sql

def get_all_group(user_id):
   user_state = "NEW"
   group_ids = []
   expense_groups = sql.get_all_expense_group(user_id)
   if len(expense_groups) == 1:
     user_state = "SINGLE_GROUP"
     for expense_group in expense_groups:
        group_ids.append(expense_group)
     return user_state, group_ids
   if len(expense_groups) > 1:
     user_state = "MULTI_GROUP"
     for expense_group in expense_groups:
       group_ids.append(expense_group) 
     return user_state,group_ids
   return user_state,group_ids

def get_all_user_by_group(group_id):
  user_id_name_map = []
  users_info = sql.get_users_by_group(group_id)
  for user_info in users_info:
    user_dict = {
      "user_name":user_info[3],
      "user_id":user_info[2]
    }
    user_id_name_map.append(user_dict)

  return user_id_name_map