import requests
from flask import Flask,session,render_template,request,redirect,g,url_for


app=Flask(__name__)
@app.route('/')
def index():
# Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your Zoom OAuth app's credentials.
    CLIENT_ID = '3wtJirnSqu1OO2Fu3Q0ew'
    CLIENT_SECRET = 'dl7abNehr3nsbKYSyyEs1OqjIsCUax9S'

    # Endpoint to redirect the user for Zoom OAuth authorization.
    AUTH_URL = 'https://zoom.us/oauth/authorize'

    # Endpoint to get the access token after user authorization.
    TOKEN_URL = 'https://zoom.us/oauth/token'

    # Redirect URL for Zoom OAuth. Replace this with your app's redirect URL.
    REDIRECT_URI = 'http://127.0.0.1:5000/'

    def get_access_token():
        # Redirect the user to Zoom OAuth for authorization.
        auth_params = {
            'response_type': 'code',
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI
        }
        auth_response = requests.get(AUTH_URL, params=auth_params)
        auth_code = input("Please authorize the app and enter the authorization code: ")

        # Exchange the authorization code for an access token.
        token_params = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI
        }
        token_response = requests.post(TOKEN_URL, data=token_params)

        if token_response.status_code == 200:
            return token_response.json()['access_token']
        else:
            print("Failed to obtain access token.")
            return None

    access_token = get_access_token()

    def create_zoom_meeting(topic, start_time, duration):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'topic': topic,
            'type': 2,  # 2 for scheduled meeting, 1 for instant meeting
            'start_time': start_time,
            'duration': duration,
        }

        response = requests.post('https://api.zoom.us/v2/users/me/meetings', json=data, headers=headers)

        if response.status_code == 201:
            meeting_info = response.json()
            return meeting_info['join_url']
        else:
            print(f"Failed to create a Zoom meeting. Error code: {response.status_code}")
            return None

    # Example usage:
    meeting_topic = "Team Meeting"
    start_time = "2023-07-24T12:00:00Z"  # Replace with your desired meeting start time in ISO 8601 format.
    meeting_duration = 60  # Meeting duration in minutes.

    join_url = create_zoom_meeting(meeting_topic, start_time, meeting_duration)
    if join_url:
        print(f"Zoom meeting created: {join_url}")
    return join_url

if __name__ == '__main__':
    app.run(debug=True)