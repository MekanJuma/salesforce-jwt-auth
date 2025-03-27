import jwt
import time
from datetime import datetime, timedelta

# Configuration
private_key = open('private_unencrypted.key', 'r').read()
consumer_key = "3MVG9DMdJCij4PmGRoL_xWsvyna0JS8en1grVfTM.GF4O.nrfPDnOlwnyHZFt_BoerJ2rDHNtAGs0I4eWIhLu"
username = "simoapp@simplifa.de.qa"
login_url = "https://test.salesforce.com"

# Create payload
payload = {
    "iss": consumer_key,
    "sub": username,
    "aud": login_url,
    "exp": int(time.time()) + (5 * 365 * 24 * 60 * 60),  # 5 years expiration
    "iat": int(time.time())
}

# Generate token
encoded_token = jwt.encode(
    payload,
    private_key,
    algorithm="RS256",
    headers={"alg": "RS256"}
)

print("SALESFORCE_SIGNED_TOKEN:", encoded_token)