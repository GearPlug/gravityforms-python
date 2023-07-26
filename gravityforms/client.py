import time

import requests
from requests_oauthlib import OAuth1

from gravityforms.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError

class Client(object):
    def __init__(self, base_url, consumer_key, consumer_secret):
        #TODO: Fix possible base_url different inputs.
        self.URL = f"{base_url}wp-json/gf/v2/"
        timestamp = str(int(time.time())+1000)
        self.oauth = OAuth1(consumer_key, client_secret=consumer_secret, timestamp=timestamp)

    def list_entries(self):
        return self.get("entries")

    def filter_entries(self, filter_field, filter_value, filter_operator, sorting_key=None, sorting_direction=None):
        query = f'entries?search={{"field_filters": [{{"key":"{filter_field}","value":"{filter_value}","operator":"{filter_operator}"}}]}}'
        if sorting_direction:
            query += f"&sorting[direction]={sorting_direction}"
        return self.get(query)

    def list_forms(self):
        return self.get("forms")

    def get_form_detail(self, form_id):
        return self.get(f"forms/{form_id}/results")

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, **kwargs):
        return requests.request(method, self.URL + endpoint, auth=self.oauth, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
