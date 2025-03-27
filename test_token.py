import json
import requests
from datetime import datetime

def load_token():
    """Load the JWT token from json file"""
    with open('token.json', 'r') as f:
        data = json.load(f)
        return data['SALESFORCE_SIGNED_TOKEN']

def get_access_token(jwt_token):
    """Exchange JWT token for Salesforce access token"""
    auth_url = 'https://test.salesforce.com/services/oauth2/token'
    params = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': jwt_token
    }
    
    response = requests.post(auth_url, params=params)
    if response.status_code == 200:
        print("✅ Authentication successful!")
        return response.json()
    else:
        print("❌ Authentication failed!")
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.text}")
        return None

def test_api_call(access_token):
    """Make a test API call to Salesforce"""
    # Get instance URL from the auth response
    instance_url = access_token['instance_url']
    
    # Set up headers with the access token
    headers = {
        'Authorization': f"Bearer {access_token['access_token']}",
        'Content-Type': 'application/json'
    }
    
    # Test API endpoint - getting user info
    api_url = f"{instance_url}/services/data/v59.0/chatter/users/me"
    
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        print("\n✅ API Call successful!")
        print(f"Authenticated as: {user_data.get('displayName', 'N/A')}")
        print(f"Email: {user_data.get('email', 'N/A')}")
        print(f"User ID: {user_data.get('id', 'N/A')}")
    else:
        print("\n❌ API Call failed!")
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.text}")

def main():
    print("🔄 Starting Salesforce API test...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Load JWT token
    print("1️⃣ Loading JWT token from token.json...")
    jwt_token = load_token()
    print("Token loaded successfully!\n")
    
    # Get access token
    print("2️⃣ Exchanging JWT token for access token...")
    access_token = get_access_token(jwt_token)
    
    if access_token:
        print("\n3️⃣ Testing API call...")
        test_api_call(access_token)
    
    print("\n✨ Test completed!")

if __name__ == "__main__":
    main() 