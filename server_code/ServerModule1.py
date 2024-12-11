import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
import re
import urllib.parse

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
    anvil.server.session["login"] = True
    return len(res), res, query, accountnumber
  else:
    return len(res), res, query, 0

@anvil.server.callable
def login_secure(username, password):
  conn = sqlite3.connect(data_files['temp_database.db'])
  cursor = conn.cursor()
  
  query = "SELECT username, password, AccountNo FROM Users WHERE username = ? AND password = ?"
  
  try:
    cursor.execute(query, (username, password))
    res = cursor.fetchall()
  except Exception as e:
    print(e)
    res = []
  
  conn.close()

  if len(res) > 0:
    accountNo = res[0][2] 
    return len(res), res, query, accountNo
  else:
    return len(res), res, query, 0



@anvil.server.callable
def get_user_by_account_no(account_no):
  # Fetch user data from the database
  user = app_tables.users.get(account_no=account_no)
  if user:
      return {'username': user['username']}
  return None

@anvil.server.callable
def get_login_state():
  if "login" not in anvil.server.session:
    anvil.server.session["login"] = False
  return anvil.server.session["login"]

@anvil.server.callable
def get_logout_state():
  if "login" in anvil.server.session:
    del anvil.server.session["login"]
  return "Erfolgreich abgemeldet"


@anvil.server.callable
def login_account(url):
  con = sqlite3.connect(data_files["temp_database.db"])
  cur = con.cursor()

  # Account-Nummer aus der URL extrahieren
  account_no = get_accountNumber_from_query(url)
  if account_no is None:
      return "Keine gültige Account-Nummer angegeben."

  try:
      # Unsichere Abfragen
      cur.execute(f"SELECT username FROM Users WHERE AccountNo = {account_no}")
      users = cur.fetchall()
      cur.execute(f"SELECT balance FROM Balances WHERE AccountNo = {account_no}")
      balances = cur.fetchall()
  except Exception as e:
      return f"Fehler bei der Abfrage: {e}"
  finally:
      con.close()

  return {"users": users, "balances": balances}


def get_accountNumber_from_query(url):
  query_string = url.split('?')[-1] if '?' in url else ''
  query_params = urllib.parse.parse_qs(query_string)
  if "AccountNo" in query_params:
      return query_params["AccountNo"][0]
  return None
  