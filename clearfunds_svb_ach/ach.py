import json
import time
import hashlib
import hmac

import requests


class SVBACH:
    ENDPOINTS = {
        "create_ach": {
            "method": "POST",
            "path": "/v1/ach",
            "query": "",
            "body": ""
        },
        "retrieve_ach": {
            "method": "GET",
            "path": "/v1/ach/%s",
            "query": "",
            "body": ""
        },
        "update_ach": {
            "method": "PATCH",
            "path": "/v1/ach/%s",
            "query": "",
            "body": ""
        },
        "list_ach": {
            "method": "GET",
            "path": "/v1/ach",
            "query": "",
            "body": ""
        },
    }

    ENVIRONMENTS = {
        "sandbox": {
            "URL": "https://uat.api.svb.com"
        },
        "production": {
            "URL": "https://api.svb.com"
        }
    }

    def __init__(self, *args, **kwargs):
        self.api_key = kwargs.get("api_key")
        self.api_secret = kwargs.get("api_secret")
        self.env = kwargs.get("env")
        self.ach_id = kwargs.get("ach_id")
        self.status = kwargs.get("status")
        self.account_number = kwargs.get("account_number")
        self.amount = kwargs.get("amount")
        self.direction = kwargs.get("direction")
        self.receiver_account_number = kwargs.get("receiver_account_number")
        self.receiver_account_type = kwargs.get("receiver_account_type")
        self.receiver_name = kwargs.get("receiver_name")
        self.receiver_routing_number = kwargs.get("receiver_routing_number")
        self.sec_code = kwargs.get("sec_code")

        self.ENVIRONMENT = self.ENVIRONMENTS.get(self.env, None)

        if not self.ENVIRONMENT:
            raise Exception("Invalid env provided")

    def _generate_request_signature(self, timestamp, method, path, query, body):
        message = "\n".join([timestamp, method, path, query, body])
        signature = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(message, 'utf-8'),
                             hashlib.sha256).hexdigest()
        return signature

    def generate_request_signature(self, endpoint, ach_id=None, body=None):
        timestamp = str(int(time.time()))
        request_endpoint = self.ENDPOINTS.get(endpoint, None)
        if not request_endpoint:
            raise Exception("Request Endpoint not defined")

        request_method = request_endpoint.get("method")
        request_path = request_endpoint.get("path")
        if ach_id:
            request_path = f'{request_path}' % ach_id
        request_query = request_endpoint.get("query")
        if not body:
            request_body = request_endpoint.get("body")
        else:
            request_body = json.dumps(body)

        signature = self._generate_request_signature(timestamp,
                                                     request_method, request_path,
                                                     request_query, request_body)

        return signature, request_path, timestamp

    def create_ach(self):
        body = {
            "data":
                {
                    "account_number": self.account_number,
                    "amount": self.amount,
                    "direction": self.direction,
                    "receiver_account_number": self.receiver_account_number,
                    "receiver_account_type": self.receiver_account_type,
                    "receiver_name": self.receiver_name,
                    "receiver_routing_number": self.receiver_routing_number,
                    "sec_code": self.sec_code
                }
        }
        endpoint = "create_ach"

        signature, request_path, timestamp = self.generate_request_signature(
            endpoint, body=body
        )

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'content-type': 'application/json',
            'X-Timestamp': timestamp,
            'X-Signature': signature
        }

        request = requests.post(
            f'{self.ENVIRONMENT.get("URL")}{request_path}',
            headers=headers, data=json.dumps(body)
        )

        return request.content

    def retrieve_ach(self):
        endpoint = "retrieve_ach"

        signature, request_path, timestamp = self.generate_request_signature(
            endpoint, ach_id=self.ach_id
        )

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'content-type': 'application/json',
            'X-Timestamp': timestamp,
            'X-Signature': signature
        }

        request = requests.get(
            f'{self.ENVIRONMENT.get("URL")}{request_path}',
            headers=headers
        )

        return request.content

    def update_ach(self):
        body = {
            "data":
                {
                    "status": self.status,
                }
        }
        endpoint = "update_ach"

        signature, request_path, timestamp = self.generate_request_signature(
            endpoint, ach_id=self.ach_id, body=body
        )

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'content-type': 'application/json',
            'X-Timestamp': timestamp,
            'X-Signature': signature
        }

        request = requests.patch(
            f'{self.ENVIRONMENT.get("URL")}{request_path}',
            headers=headers, data=json.dumps(body)
        )

        return request.content

    def list_ach(self):
        endpoint = "list_ach"

        signature, request_path, timestamp = self.generate_request_signature(endpoint)

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'content-type': 'application/json',
            'X-Timestamp': timestamp,
            'X-Signature': signature
        }

        request = requests.get(
            f'{self.ENVIRONMENT.get("URL")}{request_path}',
            headers=headers
        )

        return request.content
