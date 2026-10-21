from google_auth_oauthlib.flow import Flow
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Load client config from credentials.json
with open('credentials.json', 'r') as f:
    import json
    client_config = json.load(f)

# Use console flow (paste URL into browser manually, paste code back)
flow = Flow.from_client_config(
    client_config,
    scopes=SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

auth_url, _ = flow.authorization_url(prompt='consent')
print('\n' + '='*60)
print('STEP 1: Open this URL in your browser:')
print('='*60)
print(auth_url)
print('='*60)
print('\nSTEP 2: After authorizing, copy the authorization code')
print('STEP 3: Paste it below and press ENTER\n')

while True:
    code = input('Enter authorization code: ').strip()
    if code:
        break
    print('Code cannot be empty! Please try again.')

try:
    flow.fetch_token(code=code)
    with open('token.pickle', 'wb') as token:
        pickle.dump(flow.credentials, token)
    print('\n✅ SUCCESS - token.pickle created!')
except Exception as e:
    print(f'\n❌ ERROR: {e}')
    print('Please try again with a valid authorization code.')
    exit(1)
