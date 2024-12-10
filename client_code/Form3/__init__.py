from ._anvil_designer import Form3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.js

class Form3(Form3Template):
  def __init__(self, res, query, account_no, **properties):
    self.init_components(**properties)

    if res == "login successful":
      self.text_box_1.text = "Login successful!"
      anvil.js.window.location.hash = f"#account/{account_no}"

    elif res == "login suspicious":
      self.text_box_1.text = "Login successful but no account number was passed."
    else:
        self.text_box_1.text = f"Warnung: Login fehlgeschlagen! \nAbfrage: {query}"

  
  def Logout_Button_click(self, **event_args):
    anvil.js.window.location.hash = ""
    open_form('Form1')  
