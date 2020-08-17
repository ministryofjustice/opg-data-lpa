import boto3
import subprocess
import re
import os
import argparse
from boto3 import Session
from boto3 import exceptions


class PactDeploymentCheck:
    def __init__(
        self,
        pact_broker_url,
        broker_user_name,
        broker_secret_name,
        consumer_pacticipant,
        provider_pacticipant,
        consumer_api_version,
        git_commit,
    ):

        self.pact_broker_url = pact_broker_url
        self.broker_user_name = broker_user_name
        self.broker_secret_name = broker_secret_name
        self.consumer_pacticipant = consumer_pacticipant
        self.provider_pacticipant = provider_pacticipant
        self.consumer_api_version = consumer_api_version
        self.git_commit = git_commit
        self.broker_password = self.get_secret()

        current_folder = os.path.basename(os.path.normpath(os.getcwd()))
        if "CI" in os.environ:
            if current_folder == "test":
                self.pact_path_prefix = "../../"
            else:
                self.pact_path_prefix = "../"
        else:
            if current_folder == "test":
                self.pact_path_prefix = "../../../"
            else:
                self.pact_path_prefix = "../../"

    def can_i_deploy(self):
        # CanIDeploy with consumer git_commit and latest provider tagged with v<x>_production (must get version from tags)
        command = '''{pact_path_prefix}pact/bin/pact-broker can-i-deploy \\
            --broker-base-url=\"{pact_broker_url}\" \\
            --broker-username=\"{broker_user_name}\" \\
            --broker-password=\"{broker_password}\" \\
            --pacticipant=\"{consumer_pacticipant}\" \\
            --version \"{git_commit_consumer}\" \\
            --pacticipant \"{provider_pacticipant}\" \\
            --latest \"{latest}\"'''.format(
            pact_broker_url=self.pact_broker_url,
            broker_user_name=self.broker_user_name,
            broker_password=self.broker_password,
            consumer_pacticipant=self.consumer_pacticipant,
            provider_pacticipant=self.provider_pacticipant,
            latest=f"{self.consumer_api_version}_production",
            git_commit_consumer=self.git_commit,
            pact_path_prefix=self.pact_path_prefix,
        )

        #
        command_response = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        fail_build = True
        for line in command_response.stdout.readlines():
            if "Computer says yes" in str(line):
                fail_build = False
            pass

        ansi_escape_8bit = re.compile(
            br"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
        )
        last_line = ansi_escape_8bit.sub(b"", line)
        print(last_line)

        return fail_build

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
    parser = argparse.ArgumentParser(
        description="Check if we can continue our CI pipeline."
    )
    parser.add_argument(
        "--pact_broker_url",
        default="https://pact-broker.api.opg.service.justice.gov.uk",
        help="Base URL for the pact broker.",
    )
    parser.add_argument(
        "--broker_user_name",
        default="admin",
        help="The user to log in to pact broker with.",
    )
    parser.add_argument(
        "--broker_secret_name",
        default="pactbroker_admin",
        help="Name of the secret to use to get the password.",
    )
    parser.add_argument(
        "--consumer_pacticipant",
        default="Complete the deputy report",
        help="Name of the consumer of the API.",
    )
    parser.add_argument(
        "--provider_pacticipant",
        default="OPG Data",
        help="Name of the provider of the API.",
    )
    parser.add_argument(
        "--consumer_api_version",
        default="v1",
        help="Name of consumer version to check.",
    )
    parser.add_argument(
        "--git_commit",
        default="d31b90b",
        help="Reference for the consumer git commit version.",
    )

    args = parser.parse_args()

    deployment_check = PactDeploymentCheck(
        args.pact_broker_url,
        args.broker_user_name,
        args.broker_secret_name,
        args.consumer_pacticipant,
        args.provider_pacticipant,
        args.consumer_api_version,
        args.git_commit,
    )

    print(deployment_check.can_i_deploy())


if __name__ == "__main__":
    main()
