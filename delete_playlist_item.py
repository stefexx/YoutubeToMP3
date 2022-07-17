
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

clientID = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube','https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

credentials = None
def main():
    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)




    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                clientID,
                scopes=[
                    'https://www.googleapis.com/auth/youtube'
                ]
            )

            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message="")
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)


    #Connecting to Youtube Api with newly saved tokens
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    request = youtube.playlistItems().list(
        part="id",
        playlistId="PLedrohii4LSDxUp0hGulVO41ez-UylY07"
    )
    response = request.execute()
    print(response)

    yt_item_id = []
    for item in response['items']:
        yt_item_id.append(item['id'])

    print (yt_item_id)

    for id in yt_item_id:
        delete_request = youtube.playlistItems().delete(id=id)
        delete_request.execute()
        print("Deleted song from playlist")

if __name__ == "__main__":
    main()
#delete_items()

#having errors after seven days as the refresh token expries, google problem since the app in is "testing"
#to fix, comment out the first code block, run, and relogin in to youtube accouhtm, once authteticated, you can use for 7 days. kinda sucks though
#for the second code block, find a wAY TO AUTOMATICALY REDIREct me to the login screen, as it just spits out an error
#try changing the  publication to in production, requires a bunch a documentaion though. So maybe not
