
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
