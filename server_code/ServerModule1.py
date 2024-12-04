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
  
  query = f"SELECT username, password FROM Users WHERE username = '{username}' AND password = '{password}'"
  
  try:
    cursor.execute(query)
    res = cursor.fetchall()
  except Exception as e:
    print(e)
    res = []
  
  conn.close()
  return len(res), res, query

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

