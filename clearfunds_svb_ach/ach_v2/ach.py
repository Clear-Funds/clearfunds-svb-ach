import json
import uuid

import requests
from jwcrypto import jwk, jwt

from clearfunds_svb_ach.ach_v2.auth import ACHAuthorization


class SVBACH(ACHAuthorization):
    ENDPOINTS = {
        "create_ach": {
            "method": "POST",
            "path": "/v2/transfer/domestic-achs",
            "query": "",
            "body": ""
        },
        "retrieve_ach": {
            "method": "GET",
            "path": "/v2/transfer/domestic-achs/%s",
            "query": "",
            "body": ""
        },
        "update_ach": {
            "method": "PATCH",
            "path": "/v2/transfer/domestic-achs/%s",
            "query": "",
            "body": ""
        },
        "list_ach": {
            "method": "GET",
            "path": "/v2/transfer/domestic-achs",
            "query": "",
            "body": ""
        },
    }

    def detached_jwt(self, payload_data):
        key = jwk.JWK.from_password(self.client_secret)

        payload = json.dumps(payload_data, indent=2)
        headers = {"alg": "HS256", "kid": str(uuid.uuid4()), "typ": "JOSE"}

        # Creating the jws_token and sign
        jws_token = jwt.JWT(header=headers, claims=payload)
        jws_token.make_signed_token(key)
        sig = jws_token.serialize()

        # Detaching JWT
        splitted_JWS = sig.split(".")
        splitted_JWS[1] = ""

        return '.'.join(splitted_JWS)

    def get_request_path(self, endpoint_name, ach_id=None):
        endpoint_obj = self.ENDPOINTS.get(endpoint_name)
        if not endpoint_obj:
            raise Exception("Request Endpoint not defined")

        request_path = endpoint_obj.get("path")
        if ach_id:
            request_path = f'{request_path}' % ach_id

        return request_path

    def create_ach(self, batch_data, receiver_data, amount, date):
        body = {
            "batch_details": {
                "svb_account_number": batch_data.get('account_number'),
                "direction": batch_data.get('direction'),
                "sec_code": "CCD",
                "settlement_priority": "STANDARD",
                "effective_entry_date": date,
                "currency": "USD"
            },
            "transfers": [
                {
                    "amount": amount,
                    "receiver_account_number": receiver_data.get('account_number'),
                    "receiver_account_type": receiver_data.get('type'),
                    "receiver_name": receiver_data.get('name'),
                    "receiver_routing_number": receiver_data.get('routing_number')
                }
            ]
        }

        endpoint_name = "create_ach"
        token = self.auth_token()
        request_path = self.get_request_path(endpoint_name=endpoint_name)

        jws_signature = self.detached_jwt(body)

        headers = {
            'Authorization': f'Bearer {token}',
            'x-jws-signature': jws_signature,
            'content-type': 'application/json',
            'prefer': 'RETURN_REPRESENTATION'
        }

        request = requests.post(
            f'{self.env.get("URL")}{request_path}',
            headers=headers, data=json.dumps(body, indent=2)
        )

        return json.loads(request.content)

    def retrieve_ach(self, ach_id):
        endpoint_name = "retrieve_ach"
        token = self.auth_token()

        request_path = self.get_request_path(endpoint_name=endpoint_name, ach_id=ach_id)

        headers = {'Authorization': f'Bearer {token}'}

        request = requests.get(f'{self.env.get("URL")}{request_path}', headers=headers)

        return json.loads(request.content)

    def list_ach(self):
        endpoint_name = "list_ach"
        token = self.auth_token()

        request_path = self.get_request_path(endpoint_name=endpoint_name)

        headers = {
            'Authorization': f'Bearer {token}',
            'prefer': 'RETURN_REPRESENTATION',
        }

        request = requests.get(
            f'{self.env.get("URL")}{request_path}',
            headers=headers
        )

        return json.loads(request.content)

    def update_ach(self, ach_id, status):
        body = [
            {
                "op": "replace",
                "path": "/status",
                "value": status
            }
        ]
        endpoint_name = "update_ach"
        token = self.auth_token()
        request_path = self.get_request_path(endpoint_name=endpoint_name, ach_id=ach_id)

        jws_signature = self.detached_jwt(body)

        headers = {
            'Authorization': f'Bearer {token}',
            'x-jws-signature': jws_signature,
            'content-type': 'application/json'
        }

        request = requests.patch(
            f'{self.env.get("URL")}{request_path}',
            headers=headers, data=json.dumps(body, indent=2)
        )

        return json.loads(request.content)
