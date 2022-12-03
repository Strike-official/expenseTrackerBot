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
  print("SQL query -------> "+sql)
  print("[DB TOUCH] Added expense to food_track table ")

def register_user(group_id,user_id, user_name):  
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "insert into expense_tracker_group_user_map (group_id,user_id, username) values ('"+group_id+"','"+user_id+"','"+user_name+"')"
  mycursor.execute(sql)
  mydb.commit()
  print("SQL query -------> "+sql)
  print("[DB TOUCH] Added user "+user_id+" to group "+group_id)