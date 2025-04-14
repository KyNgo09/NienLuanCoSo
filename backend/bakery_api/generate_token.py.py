from google_auth_oauthlib.flow import InstalledAppFlow
import os

def generate_token():
    client_secret_path = os.path.join('credentials', 'client_secret.json')
    token_path = os.path.join('credentials', 'token.json')
    scopes = ['https://www.googleapis.com/auth/drive.file']

    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
    creds = flow.run_local_server(port=0)
    
    with open(token_path, 'w') as token_file:
        token_file.write(creds.to_json())
    print(f"Token đã được lưu tại {token_path}")

if __name__ == '__main__':
    generate_token()