import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#

@anvil.server.callable
def login_unsecure(username, password):
  conn = sqlite3.connect(data_files['temp_database.db'])
  cursor = conn.cursor()
  
  # Query mit accountnumber
  query = f"SELECT username, password, AccountNo FROM Users WHERE username = '{username}' AND password = '{password}'"
  
  try:
    cursor.execute(query)
    res = cursor.fetchall()
  except Exception as e:
    print(e)
    res = []
  
  conn.close()

  if len(res) > 0:
    accountnumber = res[0][2] 
    return len(res), res, query, accountnumber
  else:
    return len(res), res, query, 0

@anvil.server.callable
def login_secure(username, password):
  conn = sqlite3.connect(data_files['temp_database.db'])
  cursor = conn.cursor()
  
  query = "SELECT username, password FROM Users WHERE username = ? AND password = ?"
  
  try:
    cursor.execute(query, (username, password))
    res = cursor.fetchall()
  except Exception as e:
    print(e)
    res = []
  
  conn.close()
  return len(res), res, query


@anvil.server.callable
def get_user_by_account_no(account_no):
  conn = sqlite3.connect(data_files['temp_database.db'])
  cursor = conn.cursor()
  
  # Sichere SQL-Abfrage mit Platzhaltern
  query = "SELECT username, email FROM Users WHERE AccountNo = ?"
  
  try:
      cursor.execute(query, (account_no,))
      user = cursor.fetchone()
      if user:
          return {"username": user[0], "email": user[1]}
  except Exception as e:
      print(f"Fehler: {e}")
  finally:
      conn.close()
  
  return None
