# Salesforce JWT Token Authentication Setup

This repository contains Python scripts for generating and testing JWT tokens for Salesforce API authentication using a Connected App. Follow these steps to set up JWT-based authentication for your Salesforce application.

## Prerequisites

- Python 3.x
- OpenSSL
- A Salesforce account with administrative access
- Git

## Installation

1. Clone this repository:
```bash
git clone https://github.com/MekanJuma/salesforce-jwt-auth.git
cd salesforce-jwt-auth
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install PyJWT cryptography requests
```

## Step-by-Step Setup Process

### 1. Generate SSL Certificate and Private Key

First, we need to generate a private key and certificate for signing JWT tokens:

```bash
# Generate private key
openssl genrsa -out private.key 2048

# Create an unencrypted version of the private key (needed for JWT signing)
openssl rsa -in private.key -out private_unencrypted.key

# Generate Certificate Signing Request (CSR)
openssl req -new -key private.key -out certificate.csr

# Generate self-signed certificate
openssl x509 -req -sha256 -days 3650 -in certificate.csr -signkey private.key -out certificate.crt
```

When generating the CSR, you'll be prompted for several pieces of information. The most important is the Common Name (CN), which can be your domain name or organization name.

### 2. Set Up Salesforce Connected App

1. Log in to your Salesforce org
2. Go to Setup → App Manager → New Connected App
3. Fill in the basic information:
   - Connected App Name: Your app name
   - API Name: Will auto-populate
   - Contact Email: Your email
4. Enable OAuth Settings:
   - Enable OAuth Settings: ✓
   - Callback URL: `file:///`
   - Use digital signatures: ✓
   - Upload your `certificate.crt` file
5. Select OAuth Scopes:
   - Access and manage your data (api)
   - Perform requests on your behalf at any time (refresh_token, offline_access)
6. Save the Connected App
7. Copy the Consumer Key (you'll need this for the script)

### 3. Configure Connected App Policies

1. After saving, wait a few minutes for the app to be created
2. Go back to Setup → App Manager → Find your app
3. Click Manage → Edit Policies
4. Under OAuth Policies:
   - Permitted Users: "Admin approved users are pre-authorized"
   - IP Relaxation: "Relax IP restrictions"
5. Save the changes

### 4. Assign Permission Sets

1. Go to Setup → Permission Sets
2. Create a new Permission Set
3. Under System Permissions, enable:
   - "Access and Manage Connected Apps"
   - "Manage Auth. Providers"
4. Assign this Permission Set to relevant users

### 5. Configure the Python Script

1. Place your `private_unencrypted.key` in the same directory as `main.py`
2. Update the following variables in `main.py`:
   ```python
   consumer_key = "YOUR_CONSUMER_KEY"  # From Connected App
   username = "YOUR_SALESFORCE_USERNAME"
   login_url = "https://test.salesforce.com"  # Use https://login.salesforce.com for production
   ```

## Usage

### Generate JWT Token

Run the script to generate a JWT token:

```bash
python main.py
```

The script will generate a JWT token and save it to `token.json` file.

### Test the Token

After generating the token, you can test it using the test script:

```bash
python test_token.py
```

The test script will:
1. Load the JWT token from `token.json`
2. Exchange it for a Salesforce access token
3. Make a test API call to verify the authentication
4. Display user information if successful

Example output:
```
🔄 Starting Salesforce API test...
Time: 2024-01-24 10:30:00

1️⃣ Loading JWT token from token.json...
Token loaded successfully!

2️⃣ Exchanging JWT token for access token...
✅ Authentication successful!

3️⃣ Testing API call...
✅ API Call successful!
Authenticated as: John Doe
Email: john.doe@example.com
User ID: 005xxxxxxxxxxxxxxx

✨ Test completed!
```

## Token Details

The generated token includes:
- `iss`: Your Connected App's Consumer Key
- `sub`: The Salesforce username
- `aud`: The Salesforce login URL
- `exp`: Expiration time (5 years from creation)
- `iat`: Token creation time

## Security Notes

1. Never commit your private keys to version control
2. Keep your private key secure and restrict access to authorized personnel
3. Rotate certificates periodically (recommended annually)
4. Monitor Connected App usage in Salesforce Setup
5. The `token.json` file containing your JWT token is automatically ignored by git

## Troubleshooting

Common issues and solutions:

1. **Certificate Issues**
   - Ensure the certificate is in X.509 format
   - Verify the certificate hasn't expired
   - Check that the certificate was properly uploaded to the Connected App

2. **Authentication Errors**
   - Verify the Consumer Key is correct
   - Confirm the username has proper permissions
   - Check that the user is approved for the Connected App

3. **Token Generation Errors**
   - Ensure all required packages are installed
   - Verify the private key file is unencrypted and readable
   - Check that the algorithm specified matches the certificate type

4. **API Call Errors**
   - Verify the access token was obtained successfully
   - Check that the API version in the URL is supported
   - Ensure the user has appropriate permissions for the API endpoint



