from ._anvil_designer import AccountNoTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.js

class AccountNo(AccountNoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.update_user_data()
    anvil.js.window.addEventListener("hashchange", self.update_user_data)

  def update_user_data(self, *args):
    url = anvil.js.window.location.href
    account_info = anvil.server.call("login_account", url)
    self.username_label.text = account_info

  def Logout_btn_click(self, **event_args):
    anvil.server.call('get_logout_state')
    anvil.js.window.history.pushState({}, "Logged out", "/")
    open_form('Form1')
