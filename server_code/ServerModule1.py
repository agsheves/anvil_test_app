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

    except anvil.http.HttpError as e:
        print(f"HTTP Error creating session: {e}")
        print(f"Status code: {e.status}")

        # Try to get the response body using the correct Anvil method
        try:
            # In Anvil, we need to access the response differently
            error_response = e.response
            if error_response:
                error_body = error_response.get_bytes()
                print(f"Error response body (raw): {error_body}")

                if error_body:
                    try:
                        error_json = json.loads(error_body)
                        print(f"Parsed error response: {error_json}")

                        # Extract HeyGen specific error details
                        error_details = ""
                        if "code" in error_json:
                            error_details += f"Code: {error_json['code']}"
                        if "message" in error_json:
                            if error_details:
                                error_details += ", "
                            error_details += f"Message: {error_json['message']}"
                        if "details" in error_json:
                            if error_details:
                                error_details += ", "
                            error_details += f"Details: {error_json['details']}"

                        if error_details:
                            print(f"HeyGen error details: {error_details}")
                            return {"error": error_details}
                        else:
                            return {
                                "error": f"HTTP {e.status}: {error_body.decode('utf-8', errors='ignore')}"
                            }
                    except json.JSONDecodeError:
                        return {
                            "error": f"HTTP {e.status}: {error_body.decode('utf-8', errors='ignore')}"
                        }
                else:
                    return {"error": f"HTTP {e.status}: No response body"}
            else:
                return {"error": f"HTTP {e.status}: No response object"}

        except Exception as parse_error:
            print(f"Could not parse error response: {parse_error}")
            return {"error": f"HTTP {e.status}: Could not parse error response"}

    except Exception as e:
        print(f"Unexpected error creating session: {e}")
        return {"error": f"Unexpected error: {str(e)}"}


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
    except anvil.http.HttpError as e:
        print(f"HTTP Error starting session: {e}")
        print(f"Status code: {e.status}")

        try:
            error_response = e.response
            if error_response:
                error_body = error_response.get_bytes()
                if error_body:
                    try:
                        error_json = json.loads(error_body)
                        error_details = ""
                        if "code" in error_json:
                            error_details += f"Code: {error_json['code']}"
                        if "message" in error_json:
                            if error_details:
                                error_details += ", "
                            error_details += f"Message: {error_json['message']}"

                        if error_details:
                            return {"error": error_details}
                        else:
                            return {
                                "error": f"HTTP {e.status}: {error_body.decode('utf-8', errors='ignore')}"
                            }
                    except json.JSONDecodeError:
                        return {
                            "error": f"HTTP {e.status}: {error_body.decode('utf-8', errors='ignore')}"
                        }
                else:
                    return {"error": f"HTTP {e.status}: No response body"}
            else:
                return {"error": f"HTTP {e.status}: No response object"}

        except Exception as parse_error:
            print(f"Could not parse start error response: {parse_error}")
            return {"error": f"HTTP {e.status}: Could not parse error response"}

    except Exception as e:
        print(f"Unexpected error starting session: {e}")
        return {"error": f"Unexpected error: {str(e)}"}


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
    except anvil.http.HttpError as e:
        print(f"HTTP Error sending text: {e}")

        try:
            error_response = e.response
            if error_response:
                error_body = error_response.get_bytes()
                if error_body:
                    try:
                        error_json = json.loads(error_body)
                        error_details = ""
                        if "code" in error_json:
                            error_details += f"Code: {error_json['code']}"
                        if "message" in error_json:
                            if error_details:
                                error_details += ", "
                            error_details += f"Message: {error_json['message']}"

                        if error_details:
                            return {"error": error_details}
                        else:
                            return {
                                "error": f"HTTP {e.status}: {error_body.decode('utf-8', errors='ignore')}"
                            }
                    except json.JSONDecodeError:
                        return {
                            "error": f"HTTP {e.status}: {error_body.decode('utf-8', errors='ignore')}"
                        }
                else:
                    return {"error": f"HTTP {e.status}: No response body"}
            else:
                return {"error": f"HTTP {e.status}: No response object"}

        except Exception as parse_error:
            print(f"Could not parse send text error response: {parse_error}")
            return {"error": f"HTTP {e.status}: Could not parse error response"}

    except Exception as e:
        print(f"Unexpected error sending text: {e}")
        return {"error": f"Unexpected error: {str(e)}"}


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
    except anvil.http.HttpError as e:
        print(f"HTTP Error closing session: {e}")

        try:
            error_response = e.response
            if error_response:
                error_body = error_response.get_bytes()
                if error_body:
                    try:
                        error_json = json.loads(error_body)
                        error_details = ""
                        if "code" in error_json:
                            error_details += f"Code: {error_json['code']}"
                        if "message" in error_response:
                            if error_details:
                                error_details += ", "
                            error_details += f"Message: {error_json['message']}"

                        if error_details:
                            return {"error": error_details}
                        else:
                            return {
                                "error": f"HTTP {e.status}: {error_body.decode('utf-8', errors='ignore')}"
                            }
                    except json.JSONDecodeError:
                        return {
                            "error": f"HTTP {e.status}: {error_body.decode('utf-8', errors='ignore')}"
                        }
                else:
                    return {"error": f"HTTP {e.status}: No response body"}
            else:
                return {"error": f"HTTP {e.status}: No response object"}

        except Exception as parse_error:
            print(f"Could not parse close error response: {parse_error}")
            return {"error": f"HTTP {e.status}: Could not parse error response"}

    except Exception as e:
        print(f"Unexpected error closing session: {e}")
        return {"error": f"Unexpected error: {str(e)}"}


@anvil.server.callable
def process_user_input(user_text):
    return f"I heard you say: {user_text}. How can I help you with that?"
