import anvil.secrets
import anvil.http
import anvil.server
import json


@anvil.server.callable
def create_heygen_session(avatar_id, voice_id):
    api_key = anvil.secrets.get_secret("HEYGEN_API_KEY")
    server_url = "https://api.heygen.com"

    # First get session token
    token_response = anvil.http.request(
        f"{server_url}/v1/streaming.create_token",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
        },
    )
    token_data = json.loads(token_response.get_bytes())
    session_token = token_data["data"]["token"]

    # Then create session using that token
    session_response = anvil.http.request(
        f"{server_url}/v1/streaming.new",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_token}",
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

    return {
        "sessionInfo": session_data["data"],
        "sessionToken": session_token,  # Return the generated session token
    }


@anvil.server.callable
def start_heygen_session(session_id, session_token):
    server_url = "https://api.heygen.com"

    response = anvil.http.request(
        f"{server_url}/v1/streaming.start",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_token}",
        },
        json={"session_id": session_id},
    )
    return json.loads(response.get_bytes())


@anvil.server.callable
def send_text_to_avatar(session_id, text, session_token, task_type="talk"):
    server_url = "https://api.heygen.com"

    response = anvil.http.request(
        f"{server_url}/v1/streaming.task",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_token}",
        },
        json={"session_id": session_id, "text": text, "task_type": task_type},
    )
    return json.loads(response.get_bytes())


@anvil.server.callable
def close_heygen_session(session_id, session_token):
    server_url = "https://api.heygen.com"

    response = anvil.http.request(
        f"{server_url}/v1/streaming.stop",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_token}",
        },
        json={"session_id": session_id},
    )
    return json.loads(response.get_bytes())


@anvil.server.callable
def process_user_input(user_text):
    return f"I heard you say: {user_text}. How can I help you with that?"
