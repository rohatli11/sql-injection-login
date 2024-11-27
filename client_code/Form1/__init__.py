from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  

  def Enter_Button_click(self, **event_args):
    res, query = anvil.server.call("login", self.username_input.text, self.password_input.text)

    if not res:
        self.ausgabe_feld.text = query
    else:
        self.ausgabe_feld.text = f"Ergebnisse: {res}, Abfrage: {query}"
    
   