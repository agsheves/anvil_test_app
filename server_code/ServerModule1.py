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

  try:
    # Step 1: Create session
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
    session_data = json.loads(session_response.get_bytes())["data"]
    print(f"Session created: {session_data}")

    # Step 2: Start streaming using session access_token
    start_response = anvil.http.request(
      f"{server_url}/v1/streaming.start",
      method="POST",
      headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_data['access_token']}",
      },
      json={
        "session_id": session_data["session_id"]
      }
    )
    print("Streaming started")

    return {
      "sessionInfo": session_data
    }

  except anvil.http.HttpError as e:
    if hasattr(e.content, 'get_bytes'):
      error_body = e.content.get_bytes().decode('utf-8')
      try:
        error_data = json.loads(error_body)
      except:
        error_data = {"message": error_body}
    else:
      error_data = e.content

    raise Exception(f"HeyGen API Error {error_data.get('code', e.status)}: {error_data.get('message', 'Unknown error')}")


@anvil.server.callable
def process_user_input(user_text):
  return f"I heard you say: {user_text}. How can I help you with that?"