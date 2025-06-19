import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.secrets
import anvil.secrets
import anvil.http
import anvil.server
import json

@anvil.server.callable
def create_heygen_session(avatar_id, voice_id):
  """Create a new HeyGen session and return session info"""
  print(f"Server: Creating session for avatar={avatar_id}, voice={voice_id}")

  api_key = anvil.secrets.get_secret("HEYGEN_API_KEY")
  server_url = "https://api.heygen.com"

  # Get session token
  token_response = anvil.http.request(
    f"{server_url}/v1/streaming.create_token",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "X-Api-Key": api_key,
    }
  )
  session_token = token_response.json()["data"]["token"]

  # Create new session
  session_response = anvil.http.request(
    f"{server_url}/v1/streaming.new",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "Authorization": f"Bearer {session_token}",
    },
    json={
      "quality": "high",
      "avatar_name": avatar_id,
      "voice": {
        "voice_id": voice_id,
        "rate": 1.0,
      },
      "version": "v2",
      "video_encoding": "H264",
    }
  )
  print(session_response)
  return {
    "sessionInfo": session_response.json()["data"],
    "sessionToken": session_token
  }

@anvil.server.callable
def start_heygen_session(session_id):
  # Implementation here
  pass

@anvil.server.callable  
def process_user_input(user_text):
  # Implementation here
  return f"You said: {user_text}"

@anvil.server.callable
def send_text_to_avatar(session_id, text):
  # Implementation here
  pass

@anvil.server.callable
def close_heygen_session(session_id):
  # Implementation here
  pass