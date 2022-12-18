import mysql.connector
import uuid
import config

mydb = mysql.connector.connect(
  host=config.mysql_config["host"],
  user=config.mysql_config["user"],
  password=config.mysql_config["password"],
  database=config.mysql_config["db"]
)

def get_expense(group_id):
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM expense_tracker where group_id='"+group_id+"';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched expense details")
  return myresult

def get_all_expense_group(user_id):
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM expense_tracker_group_user_map where user_id='"+user_id+"';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] get_all_expense_group")
  return myresult

def get_expense_user_map():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT user_id,group_id FROM expense_tracker_group_user_map;")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] get_all_expense_group")
  return myresult

def get_users_by_group(group_id):
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("select * from expense_tracker_group_user_map where group_id='"+group_id+"';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched group members of group "+group_id)
  return myresult

def add_expense(user_id_of_updater,group_id,amount_paid,category,discription,split_method,who_paid,split_among):  
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "insert into expense_tracker (user_id_of_updater,group_id,amount_paid,category,discription,split_method,who_paid,split_among) values ('"+user_id_of_updater+"','"+group_id+"',"+amount_paid+",'"+category+"','"+discription+"','"+split_method+"','"+who_paid+"','"+split_among+"')"
  mycursor.execute(sql)
  mydb.commit()
  last_row_id = mycursor.lastrowid
  print(last_row_id)
  print("SQL query -------> "+sql)
  print("[DB TOUCH] Added expense to food_track table ")
  return last_row_id

def register_user(group_id,user_id, user_name):  
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "insert into expense_tracker_group_user_map (group_id,user_id, username) values ('"+group_id+"','"+user_id+"','"+user_name+"')"
  mycursor.execute(sql)
  mydb.commit()
  print("SQL query -------> "+sql)
  print("[DB TOUCH] Added user "+user_id+" to group "+group_id)

def add_expense_to_ledger(expense_id, group_id, who_paid_id, for_whom_id, individual_amount):  
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "insert into expense_tracker_ledger (expense_id, group_id, who_paid_id, for_whom_id, amount) values ('"+str(expense_id)+"','"+str(group_id)+"','"+str(who_paid_id)+"','"+str(for_whom_id)+"','"+str(individual_amount)+"');"
  print("SQL query -------> "+sql)
  mycursor.execute(sql)
  mydb.commit()
  print("[DB TOUCH] Added expense to food_track table ")
  return None

def get_expense_from_ledger():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("select group_id,who_paid_id,for_whom_id,amount from expense_tracker_ledger where if_paid='false';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched get_expense_from_ledger")
  return myresult

def tempSql():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("select group_id,amount_paid,who_paid,split_among,id from expense_tracker where group_id='SM Silver Oak';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched get_expense_from_ledger")
  return myresult