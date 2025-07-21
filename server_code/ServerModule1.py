import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.background_task
def update_courses():
  golf_files = app_files.golf_test
  ws = golf_files["Sheet1"]
  for r in ws.rows:
    name = r['name']
    #image = r['image']
    booking_time_days = r['booking_time_days']
    app_tables.course_info.add_row(name=name, booking_time_days=booking_time_days)

