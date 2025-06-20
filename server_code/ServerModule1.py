import anvil.secrets
import anvil.http
import anvil.server
import json

# Rolled back to earlier version
@anvil.server.callable
def create_heygen_session(avatar_id, voice_id):
  print("Creating Session")
  api_key = anvil.secrets.get_secret("HEYGEN_API_KEY")
  server_url = "https://api.heygen.com"

  # First get session token
  try:
    token_response = anvil.http.request(
      f"{server_url}/v1/streaming.create_token",
      method="POST",
      headers={
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
      }
    )
    token_data = json.loads(token_response.get_bytes())
    session_token = token_data["data"]["token"]
    print(f"Session token {session_token}")
  
    # Then create session using that token
    session_response = anvil.http.request(
      f"{server_url}/v1/streaming.new",
      method="POST",
      headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
      },
      json={
        "version": "v2",
        "avatar_id": avatar_id
      }
    )
    
    session_data = json.loads(session_response.get_bytes())
    print(f"Session data {session_data}")
  
    return {
      "sessionInfo": session_data["data"],
      "sessionToken": session_token  # Return the generated session token
    }
  except anvil.http.HttpError as e:
    if hasattr(e.content, 'get_bytes'):
      error_body = e.content.get_bytes().decode('utf-8')
      error_data = json.loads(error_body)
    else:
      error_data = e.content

    raise Exception(f"HeyGen API Error {error_data.get('code', e.status)}: {error_data.get('message', 'Unknown error')}")

@anvil.server.callable
def start_heygen_session(session_id):
  print("Starting session")
  api_key = anvil.secrets.get_secret("HEYGEN_API_KEY")
  server_url = "https://api.heygen.com"

  response = anvil.http.request(
    f"{server_url}/v1/streaming.start",
    method="POST",
    headers={
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}",
    },
    json={"session_id": session_id}
  )
  print(f"Session data {response}")
  return json.loads(response.get_bytes())

@anvil.server.callable
def process_user_input(user_text):
  return f"I heard you say: {user_text}. How can I help you with that?"