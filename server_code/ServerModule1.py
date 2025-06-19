import anvil.secrets
import anvil.http
import anvil.server
import json


@anvil.server.callable
def create_heygen_session(avatar_id, voice_id):
    print("Starting session")
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
        error_details = "Unknown error"

        # Try to get detailed error information
        if hasattr(e, "get_bytes"):
            try:
                error_response = json.loads(e.get_bytes())
                print(f"Full error response: {error_response}")

                # Extract HeyGen specific error details
                if "code" in error_response:
                    error_details = f"Code: {error_response['code']}"
                if "message" in error_response:
                    error_details += f", Message: {error_response['message']}"
                if "details" in error_response:
                    error_details += f", Details: {error_response['details']}"

            except Exception as parse_error:
                print(f"Could not parse error response: {parse_error}")
                error_details = f"HTTP Error: {e}"

        print(f"Detailed error: {error_details}")
        return {"error": error_details}


@anvil.server.callable
def start_heygen_session(session_id, session_token):
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
        error_details = "Unknown error"

        if hasattr(e, "get_bytes"):
            try:
                error_response = json.loads(e.get_bytes())
                print(f"Start session error response: {error_response}")

                if "code" in error_response:
                    error_details = f"Code: {error_response['code']}"
                if "message" in error_response:
                    error_details += f", Message: {error_response['message']}"

            except Exception as parse_error:
                print(f"Could not parse start error response: {parse_error}")
                error_details = f"HTTP Error: {e}"

        print(f"Start session detailed error: {error_details}")
        return {"error": error_details}


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
        error_details = "Unknown error"

        if hasattr(e, "get_bytes"):
            try:
                error_response = json.loads(e.get_bytes())
                print(f"Send text error response: {error_response}")

                if "code" in error_response:
                    error_details = f"Code: {error_response['code']}"
                if "message" in error_response:
                    error_details += f", Message: {error_response['message']}"

            except Exception as parse_error:
                print(f"Could not parse send text error response: {parse_error}")
                error_details = f"HTTP Error: {e}"

        print(f"Send text detailed error: {error_details}")
        return {"error": error_details}


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
        error_details = "Unknown error"

        if hasattr(e, "get_bytes"):
            try:
                error_response = json.loads(e.get_bytes())
                print(f"Close session error response: {error_response}")

                if "code" in error_response:
                    error_details = f"Code: {error_response['code']}"
                if "message" in error_response:
                    error_details += f", Message: {error_response['message']}"

            except Exception as parse_error:
                print(f"Could not parse close error response: {parse_error}")
                error_details = f"HTTP Error: {e}"

        print(f"Close session detailed error: {error_details}")
        return {"error": error_details}


@anvil.server.callable
def process_user_input(user_text):
    return f"I heard you say: {user_text}. How can I help you with that?"
