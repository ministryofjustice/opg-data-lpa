import boto3
import requests
import argparse
import json
import urllib.parse
from boto3 import Session
from boto3 import exceptions


class PactTagPacticipant:
    def __init__(
        self,
        pact_broker_url,
        broker_user_name,
        broker_secret_name,
        pacticipant,
        tag,
        git_commit,
    ):

        self.pact_broker_url = pact_broker_url
        self.broker_user_name = broker_user_name
        self.broker_secret_name = broker_secret_name
        self.pacticipant = pacticipant
        self.tag = tag
        self.git_commit = git_commit
        self.broker_password = self.get_secret()

    def tag_pacticipant_version(self):
        full_url = f"{self.pact_broker_url}/pacticipants/{self.pacticipant}/versions/{self.git_commit}/tags/{self.tag}"
        headers = {"Content-Type": "application/json"}
        pact_response = requests.put(
            full_url,
            None,
            auth=(self.broker_user_name, self.broker_password),
            headers=headers,
        )

        if pact_response.status_code <= 399:
            tagged = True
            print(
                f"Tagged pacticipant {self.pacticipant} with version {self.git_commit} correctly with : {self.tag}"
            )
        else:
            tagged = False
            print(
                f"Could not tag pacticipant {self.pacticipant} with version {self.git_commit}"
            )
            print(f"Status Code: {pact_response.status_code}")
        return tagged

    def can_tag_pacticipant_version(self):
        full_url = f"{self.pact_broker_url}/pacticipants/{self.pacticipant}/versions/{self.git_commit}"
        pact_response = requests.get(
            full_url, auth=(self.broker_user_name, self.broker_password)
        )

        if pact_response.status_code == 200:
            can_tag = True
            tags = [
                tag["name"]
                for tag in json.loads(pact_response.text)["_embedded"]["tags"]
            ]
            if len(tags) == 0:
                print("Consumer has no Tags")
            else:
                for tag in tags:
                    if tag == self.tag:
                        can_tag = False
                        print(f"Tag {self.tag} already exists")
        else:
            can_tag = False

        return can_tag

    def get_secret(self):
        """
        Gets the secret for PACT broker
        """

        if self.broker_secret_name == "local":
            return "dummy_password"

        region_name = "eu-west-1"

        client = boto3.client("sts")
        account_id = client.get_caller_identity()["Account"]
        print(f"Current users account: {account_id}")

        role_to_assume = "arn:aws:iam::997462338508:role/get-pact-secret-production"
        response = client.assume_role(
            RoleArn=role_to_assume, RoleSessionName="assumed_role"
        )

        session = Session(
            aws_access_key_id=response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
            aws_session_token=response["Credentials"]["SessionToken"],
        )

        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.broker_secret_name
            )
            secret = get_secret_value_response["SecretString"]
        except exceptions.ClientError as e:
            print("Unable to get secret from Secrets Manager")
            raise e

        return secret


def main():
    parser = argparse.ArgumentParser(description="Tag pact version with specific tag.")
    parser.add_argument(
        "--pact_broker_url",
        default="http://localhost:9292",
        help="Base URL for the pact broker.",
    )
    parser.add_argument(
        "--broker_user_name",
        default="admin",
        help="The user to log in to pact broker with.",
    )
    parser.add_argument(
        "--broker_secret_name",
        default="local",
        help="Name of the secret to use to get the password.",
    )
    parser.add_argument(
        "--pacticipant",
        default="OPGExampleApp",
        help="Name of the Pacticipant to tag.",
    )
    parser.add_argument(
        "--tag", default="v1", help="Name of tag to apply.",
    )
    parser.add_argument(
        "--git_commit", default="x123456", help="Reference for the git commit version.",
    )

    args = parser.parse_args()
    pacticipant = urllib.parse.unquote(args.pacticipant)
    tag_pact = PactTagPacticipant(
        args.pact_broker_url,
        args.broker_user_name,
        args.broker_secret_name,
        pacticipant,
        args.tag,
        args.git_commit,
    )

    if tag_pact.can_tag_pacticipant_version():
        tagged = tag_pact.tag_pacticipant_version()
        if tagged:
            print("Everything worked correctly. Exiting")


if __name__ == "__main__":
    main()
