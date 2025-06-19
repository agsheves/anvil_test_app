import anvil.secrets
import anvil.http
import anvil.server
import json


@anvil.server.callable
def create_heygen_session(avatar_id, voice_id):
    print("Creating session")
    api_key = anvil.secrets.get_secret("HEYGEN_API_KEY")
    server_url = "https://api.heygen.com"

    # Create session using API key (as per HeyGen docs)
    try:
        session_response = anvil.http.request(
            f"{server_url}/v1/streaming.new",
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "version": "v2",
                "avatar_id": avatar_id,
                "voice": {
                    "voice_id": voice_id,
                    "rate": 1.0,
                },
                "quality": "high",
                "video_encoding": "H264",
            },
        )

        session_data = json.loads(session_response.get_bytes())
        print(f"Session data: {session_data}")

        return {
            "sessionInfo": session_data["data"],
            "sessionToken": api_key,  # Use API key for subsequent HeyGen API calls
        }

    except Exception as e:
        print(f"Error creating session: {e}")
        if hasattr(e, "get_bytes"):
            error_response = json.loads(e.get_bytes())
            print(f"Error response: {error_response}")
        return None


@anvil.server.callable
def start_heygen_session(session_id, session_token):
    print("Starting session")
    server_url = "https://api.heygen.com"

    try:
        response = anvil.http.request(
            f"{server_url}/v1/streaming.start",
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {session_token}",  # This is the API key
            },
            json={"session_id": session_id},
        )
        return json.loads(response.get_bytes())
    except Exception as e:
        print(f"Error starting session: {e}")
        if hasattr(e, "get_bytes"):
            error_response = json.loads(e.get_bytes())
            print(f"Error response: {error_response}")
        return None


@anvil.server.callable
def send_text_to_avatar(session_id, text, session_token, task_type="talk"):
    server_url = "https://api.heygen.com"

    try:
        response = anvil.http.request(
            f"{server_url}/v1/streaming.task",
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {session_token}",  # This is the API key
            },
            json={"session_id": session_id, "text": text, "task_type": task_type},
        )
        return json.loads(response.get_bytes())
    except Exception as e:
        print(f"Error sending text: {e}")
        if hasattr(e, "get_bytes"):
            error_response = json.loads(e.get_bytes())
            print(f"Error response: {error_response}")
        return None


@anvil.server.callable
def close_heygen_session(session_id, session_token):
    server_url = "https://api.heygen.com"

    try:
        response = anvil.http.request(
            f"{server_url}/v1/streaming.stop",
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {session_token}",  # This is the API key
            },
            json={"session_id": session_id},
        )
        return json.loads(response.get_bytes())
    except Exception as e:
        print(f"Error closing session: {e}")
        if hasattr(e, "get_bytes"):
            error_response = json.loads(e.get_bytes())
            print(f"Error response: {error_response}")
        return None


@anvil.server.callable
def process_user_input(user_text):
    return f"I heard you say: {user_text}. How can I help you with that?"
