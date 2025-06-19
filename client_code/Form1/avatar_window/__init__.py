from ._anvil_designer import avatar_windowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class avatar_window(avatar_windowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Set up event handlers for HTML elements
        self.dom_nodes["start-btn"].addEventListener("click", self._handle_start_click)
        self.dom_nodes["close-btn"].addEventListener("click", self._handle_close_click)
        self.dom_nodes["send-btn"].addEventListener("click", self._handle_send_click)

    def _handle_start_click(self, event):
        """Handle start button click"""
        avatar_id = self.dom_nodes["avatar-input"].value
        voice_id = self.dom_nodes["voice-input"].value

        # Call server function
        session_data = anvil.server.call("create_heygen_session", avatar_id, voice_id)

        # Check if session creation was successful
        if session_data is None or "error" in session_data:
            # Show error in status
            error_message = (
                session_data.get(
                    "error",
                    "Failed to create session. Please check your avatar ID and voice ID.",
                )
                if session_data
                else "Failed to create session. Please check your avatar ID and voice ID."
            )
            self.call_js(
                "window.avatarFunctions.showError",
                error_message,
            )
            return

        # Pass data to JavaScript
        self.call_js(
            "window.avatarFunctions.setupLiveKitRoom",
            session_data["sessionInfo"],
            session_data["sessionToken"],
        )

        # Start the session with session token
        start_result = anvil.server.call(
            "start_heygen_session",
            session_data["sessionInfo"]["session_id"],
            session_data["sessionToken"],
        )

        if start_result is None or "error" in start_result:
            # Show error in status
            error_message = (
                start_result.get("error", "Failed to start session.")
                if start_result
                else "Failed to start session."
            )
            self.call_js("window.avatarFunctions.showError", error_message)
            return

        self.call_js("window.avatarFunctions.connectToRoom")

    def _handle_close_click(self, event):
        """Handle close button click"""
        self.call_js("window.avatarFunctions.closeSession")

    def _handle_send_click(self, event):
        """Handle send button click"""
        text = self.dom_nodes["task-input"].value
        if text.strip():
            # Process through AI
            response = anvil.server.call("process_user_input", text)

            # Send to avatar
            # Note: You'll need the session_id here - might need to store it

            # Show AI response
            self.call_js("window.avatarFunctions.showAIResponse", response)

            # Clear input
            self.dom_nodes["task-input"].value = ""
