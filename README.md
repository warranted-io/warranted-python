# warranted-python
A helper library for using the Warranted.io API.

## Installation
`pip install warranted`

### Test your installation
To make sure the installation was successful, try hitting the `/api/v1/me` API, like this:
```python
import os
from warranted import Client

# Get your Account Id and Auth Token from https://app.warranted.io/settings/webhook
account_id = os.environ['WARRANTED_ACCOUNT_ID']
auth_token = os.environ['WARRANTED_AUTH_TOKEN']
warranted_client = Client(account_id, auth_token)

# Fetch and print the response object
response = warranted_client.me.get()
print(response)
```

## Usage
Check out [our docs](https://app.warranted.io/docs) for more details.