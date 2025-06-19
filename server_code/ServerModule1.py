import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.secrets


@anvil.server.callable
def create_heygen_session(avatar_id, voice_id):
  """Create a new HeyGen session and return session info"""
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

  return {
    "sessionInfo": session_response.json()["data"],
    "sessionToken": session_token
  }

@anvil.server.callable
def start_heygen_session(session_id):
  """Start the HeyGen streaming session"""
  api_key = anvil.secrets.get_secret("HEYGEN_API_KEY")
  server_url = "https://api.heygen.com"

  # Note: You'll need to store the session_token globally or pass it
  # For now, get a new token (not ideal, but works)
  token_response = anvil.http.request(
    f"{server_url}/v1/streaming.create_token",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "X-Api-Key": api_key,
    }
  )
  session_token = token_response.json()["data"]["token"]

  response = anvil.http.request(
    f"{server_url}/v1/streaming.start",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "Authorization": f"Bearer {session_token}",
    },
    json={"session_id": session_id}
  )
  return response.json()

@anvil.server.callable
def send_text_to_avatar(session_id, text):
  """Send text to the avatar to speak"""
  api_key = anvil.secrets.get_secret("HEYGEN_API_KEY")
  server_url = "https://api.heygen.com"

  # Get token (again, not ideal - see note below)
  token_response = anvil.http.request(
    f"{server_url}/v1/streaming.create_token",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "X-Api-Key": api_key,
    }
  )
  session_token = token_response.json()["data"]["token"]

  response = anvil.http.request(
    f"{server_url}/v1/streaming.task",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "Authorization": f"Bearer {session_token}",
    },
    json={
      "session_id": session_id,
      "text": text,
      "task_type": "talk"
    }
  )
  return response.json()

@anvil.server.callable
def close_heygen_session(session_id):
  """Close the HeyGen session"""
  api_key = anvil.secrets.get_secret("HEYGEN_API_KEY")
  server_url = "https://api.heygen.com"

  # Get token
  token_response = anvil.http.request(
    f"{server_url}/v1/streaming.create_token",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "X-Api-Key": api_key,
    }
  )
  session_token = token_response.json()["data"]["token"]

  response = anvil.http.request(
    f"{server_url}/v1/streaming.stop",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "Authorization": f"Bearer {session_token}",
    },
    json={"session_id": session_id}
  )
  return response.json()

@anvil.server.callable
def process_user_input(user_text):
  """Process user input through your AI model"""
  # Replace this with your actual AI processing
  # Examples:

  # Simple echo for testing:
  # return f"You said: {user_text}"

  # OpenAI example:
  # import openai
  # openai.api_key = anvil.secrets.get_secret("OPENAI_API_KEY")
  # response = openai.ChatCompletion.create(...)
  # return response.choices[0].message.content

  # For now, just return a simple response
  return f"I heard you say: {user_text}. How can I help you with that?"