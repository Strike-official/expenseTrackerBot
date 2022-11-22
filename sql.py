import mysql.connector
import uuid
import config

mydb = mysql.connector.connect(
  host=config.mysql_config["host"],
  user=config.mysql_config["user"],
  password=config.mysql_config["password"],
  database=config.mysql_config["db"]
)

def get_ambulance_data():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM med_alert_ambulance_details;")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched ambulance details")
  return myresult

def update_ambulance_state(state,vehicle_number):
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "UPDATE med_alert_ambulance_details SET state = '"+state+"' WHERE vehicle_number = '"+vehicle_number+"'"
  mycursor.execute(sql)
  mydb.commit()
  print("[DB TOUCH] updated status of "+vehicle_number+" to "+state)

def get_available_ambulance():
  mydb.reconnect()
  mycursor = mydb.cursor()
  mycursor.execute("select * from med_alert_ambulance_details where state='available';")
  myresult = mycursor.fetchall()
  mydb.commit()
  print("[DB TOUCH] fetched available ambulances")
  return myresult

def add_expense(user_id_of_updater,group_id,amount_paid,category,discription,split_method):  
  mydb.reconnect()
  mycursor = mydb.cursor()
  sql = "insert into expense_tracker (user_id_of_updater,group_id,amount_paid,category,discription,split_method) values ('"+user_id_of_updater+"','"+group_id+"',"+amount_paid+",'"+category+"','"+discription+"','"+split_method+"')"
  mycursor.execute(sql)
  mydb.commit()
  print("SQL query -------> "+sql)
  print("[DB TOUCH] Added expense to food_track table ")