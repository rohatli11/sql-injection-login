from ._anvil_designer import Form3Template
from anvil import *
import anvil.server
import anvil.js
from anvil.js.window import location
import re

class Form3(Form3Template):
  def __init__(self, res, query, account_no, **properties):
    self.init_components(**properties)

    # AccountNo aus der URL holen und validieren
    account_no_from_url = self.get_account_no_from_url()
    if account_no_from_url:
      # AccountNo validieren
      if self.is_valid_account_no(account_no_from_url):
        # Daten vom Server abrufen
        user_data = anvil.server.call("get_user_by_account_no", account_no_from_url)
        if user_data:
          self.text_box_1.text = f"Willkommen zurück, {user_data['username']}!"
        else:
          self.text_box_1.text = "Kein Benutzer mit dieser Account-Nummer gefunden."
      else:
        self.text_box_1.text = "Ungültige Account-Nummer in der URL!"
    elif res == "login successful":
      self.text_box_1.text = "Login successful!"
      location.hash = f"?AccountNo={account_no}"
    elif res == "login suspicious":
      self.text_box_1.text = "Login successful but no account number was passed."
    else:
      self.text_box_1.text = f"Warnung: Login fehlgeschlagen! \nAbfrage: {query}"

  def Logout_Button_click(self, **event_args):
    location.search = ""
    open_form('Form1')

  def get_account_no_from_url(self):
    """Liest AccountNo aus der URL"""
    search_params = location.search
    if search_params.startswith("?AccountNo="):
      return search_params[len("?AccountNo="):]
    return None

  def is_valid_account_no(self, account_no):
    """Validiert die AccountNo (z. B. nur Zahlen erlaubt)"""
    return re.fullmatch(r"\d{1,20}", account_no) is not None
