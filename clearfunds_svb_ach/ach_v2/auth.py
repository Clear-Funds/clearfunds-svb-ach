import json

import requests

from base64 import b64encode


class ACHAuthorization:
    ENVIRONMENT = {
        "sandbox": {
            "URL": "https://uat.api.svb.com"
        },
        "production": {
            "URL": "https://api.svb.com"
        }
    }
    request_method = "POST"
    request_endpoint = "/v1/security/oauth/token"

    def __init__(self, **kwargs):
        self.client_id = kwargs.get("client_id")
        self.client_secret = kwargs.get("client_secret")
        self.env = self.ENVIRONMENT.get(kwargs.get("env"))

        if not self.env:
            raise Exception("Invalid env provided")

    def generate_auth_token(self):
        data = {"grant_type": "client_credentials"}

        userpass = f"{self.client_id}:{self.client_secret}"
        encoded_u = b64encode(userpass.encode()).decode()

        headers = {
            "Authorization": "Basic %s" % encoded_u,
            'content-type': 'application/x-www-form-urlencoded',
        }

        request = requests.post(
            f'{self.env.get("URL")}{self.request_endpoint}',
            headers=headers,
            data=data)

        return json.loads(request.content)

    def auth_token(self):
        content = self.generate_auth_token()
        if content.get("error"):
            raise Exception(content.get("error_description"))
        return content.get("access_token")
