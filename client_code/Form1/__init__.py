from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import location


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any cstate = anvil.server.call('get_login_state')
    

  

  def Enter_Button_click(self, **event_args):
    if self.sql_not_possible.checked:
      count, res, query, acoount_no = anvil.server.call("login_secure", self.username_input.text, self.password_input.text)
      if count == 1:
        self.ausgabe_feld.text = "Login erfolgreich!"
        location.hash = f"?AccountNo={acoount_no}"
        open_form('Form3', "login successful", query, acoount_no)
      elif count > 1:
        self.ausgabe_feld.text = "Login erfolgreich, aber mehrere Benutzer gefunden!"
        open_form('Form3', "login suspicious", query, acoount_no)
      else:
        self.ausgabe_feld.text = f"Login fehlgeschlagen!: {query}"
    
    else:
      count, res, query, acoount_no = anvil.server.call("login_unsecure", self.username_input.text, self.password_input.text)
    
      if count == 1:
        self.ausgabe_feld.text = "Login erfolgreich!"
        location.hash = f"?AccountNo={acoount_no}"
        open_form('Form3', "login successful", query, acoount_no)
      elif count > 1:
        self.ausgabe_feld.text = "Login erfolgreich, aber mehrere Benutzer gefunden!"
        open_form('Form3', "login suspicious", query, acoount_no)
      else:
        self.ausgabe_feld.text = f"Login fehlgeschlagen!: {query}"
      
   

    
   