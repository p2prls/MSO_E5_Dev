import requests as req
import json, sys, time, os

# Use environment variables from GitHub Secrets
client_id = os.getenv("CONFIG_ID")
client_secret = os.getenv("CONFIG_KEY")

# Path to save updated refresh token
path = sys.path[0] + r'/Secret.txt'
num1 = 0

def gettoken(refresh_token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    response = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    jsontxt = json.loads(response.text)

    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']

    # Save new refresh token
    with open(path, 'w+') as f:
        f.write(refresh_token)
    return access_token

def main():
    global num1
    with open(path, "r+") as fo:
        refresh_token = fo.read()

    localtime = time.asctime(time.localtime(time.time()))
    access_token = gettoken(refresh_token)

    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }

    urls = [
        'https://graph.microsoft.com/v1.0/me/drive/root',
        'https://graph.microsoft.com/v1.0/me/drive',
        'https://graph.microsoft.com/v1.0/drive/root',
        'https://graph.microsoft.com/v1.0/users',
        'https://graph.microsoft.com/v1.0/me/messages',
        'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
        'https://graph.microsoft.com/v1.0/me/drive/root/children',
        'https://api.powerbi.com/v1.0/myorg/apps',
        'https://graph.microsoft.com/v1.0/me/mailFolders',
        'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
    ]

    try:
        for url in urls:
            if req.get(url, headers=headers).status_code == 200:
                num1 += 1
                print("Successful Call:", num1)
        print('Completed:', localtime)
    except Exception as e:
        print("Error during API calls:", e)

for _ in range(5):
    main()
