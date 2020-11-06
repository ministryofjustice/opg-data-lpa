import json
from tenacity import retry
import requests

url = "http://0.0.0.0:4566/?Action=CreateSecret"


payload = {
    "Name": "local/jwt-key",
    "Description": "Secret for local testing with Docker",
    "SecretString": "this_is_a_secret_string",
    "ClientRequestToken": "EXAMPLE1-90ab-cdef-fedc-ba987SECRET1",
}

headers = {"Content-Type": "application/json"}


@retry
def insert_secret():
    print("Trying....")
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if response.status_code > 300:
        print("Container not ready yet")
        raise ConnectionError
    else:
        print(response.text.encode("utf8"))


insert_secret()
