import subprocess
import boto3
import requests
import argparse
import json
import re
import os
import urllib.parse
from boto3 import Session
from boto3 import exceptions


class PactDeploymentCheck:
    def __init__(
        self,
        provider_base_url,
        provider_custom_header,
        pact_broker_url,
        broker_user_name,
        broker_secret_name,
        consumer_pacticipant,
        provider_pacticipant,
        api_version,
        git_commit_consumer,
        git_commit_provider,
    ):

        self.provider_base_url = provider_base_url
        self.provider_custom_header = provider_custom_header
        self.pact_broker_url = pact_broker_url
        self.broker_user_name = broker_user_name
        self.broker_secret_name = broker_secret_name
        self.consumer_pacticipant = consumer_pacticipant
        self.provider_pacticipant = provider_pacticipant
        self.api_version = api_version
        self.git_commit_consumer = git_commit_consumer
        self.git_commit_provider = git_commit_provider

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

    def consumer_can_i_deploy(self):

        broker_password = self.get_secret(self.broker_secret_name)

        success, consumer_api_version = self.get_consumer_version(
            self.pact_broker_url,
            self.consumer_pacticipant,
            self.git_commit_consumer,
            self.broker_user_name,
            broker_password,
        )
        if not success:
            return consumer_api_version

        # CanIDeploy with consumer git_commit and latest provider tagged with v<x>_production (must get version from tags)
        can_i_deploy, last_line = self.run_can_i_deploy(
            pact_broker_url=self.pact_broker_url,
            broker_user_name=self.broker_user_name,
            broker_password=broker_password,
            consumer_pacticipant=self.consumer_pacticipant,
            git_commit_consumer=self.git_commit_consumer,
            provider_pacticipant=self.provider_pacticipant,
            latest=f"{consumer_api_version}_production",
        )

        if "There is no verified pact" in last_line:
            print("Running verification as this is a new pact!")
            # New Pact has not been verified before. We must verify it!
            # Verify this commit against what is in master using this providers GIT_SHA
            # Tag provider with latest version tag (this may be different to what version is being passed from digideps)
            # This is intended as we only want to allow changes that will work against the 'live' provider
            # There is an issue that what we're comparing against may be in master but not prod but it's a fringe case

            failed_verify, message = self.run_pact_verifier(
                provider_base_url=self.provider_base_url,
                custom_header=self.provider_custom_header,
                pact_broker_url=self.pact_broker_url,
                broker_user_name=self.broker_user_name,
                broker_password=broker_password,
                provider=self.provider_pacticipant,
                consumer_api_version=consumer_api_version,
                git_commit_provider=self.git_commit_provider,
            )

            print("Rerunning canideploy now pact has been verified")
            can_i_deploy, last_line = self.run_can_i_deploy(
                pact_broker_url=self.pact_broker_url,
                broker_user_name=self.broker_user_name,
                broker_password=broker_password,
                consumer_pacticipant=self.consumer_pacticipant,
                git_commit_consumer=self.git_commit_consumer,
                provider_pacticipant=self.provider_pacticipant,
                latest=f"{consumer_api_version}_production",
            )

        if (
            f"No version with tag {consumer_api_version} exists for {self.provider_pacticipant}"
            in last_line
        ):
            message, fail_build, pact_msg = (
                f"Consumer Side 'Can I Deploy' Failed! No matching provider pact with {consumer_api_version} tag!",
                True,
                last_line,
            )
        elif (
            f"No version with tag {consumer_api_version}_production exists for {self.provider_pacticipant}"
            in last_line
        ):
            message, fail_build, pact_msg = (
                f"Consumer Side 'Can I Deploy' Failed! No matching provider pact with {consumer_api_version}_production tag!",
                True,
                last_line,
            )
        elif (
            f"No pacts or verifications have been published for version {self.git_commit_consumer} of {self.provider_pacticipant}"
            in last_line
        ):
            message, fail_build, pact_msg = (
                f"Consumer Side 'Can I Deploy' Failed! No pacts or verifications have been published for version {self.git_commit_consumer}",
                True,
                last_line,
            )
        elif "failed" in last_line:
            message, fail_build, pact_msg = (
                "Consumer Side 'Can I Deploy' Failed!",
                True,
                last_line,
            )
        elif "successful" in last_line:
            message, fail_build, pact_msg = (
                "Consumer Side 'Can I Deploy' Successful",
                False,
                last_line,
            )
        else:
            message, fail_build, pact_msg = (
                "Consumer Side 'Can I Deploy' returned unknown response",
                True,
                last_line,
            )

        return message, fail_build, pact_msg

    def provider_can_i_deploy(self):

        broker_password = self.get_secret(self.broker_secret_name)
        fallback_tag = False

        api_version = os.getenv("API_VERSION")
        if api_version is None or len(api_version) == 0:
            api_version = "v1"

        failed_verify, message = self.run_pact_verifier(
            provider_base_url=self.provider_base_url,
            custom_header=self.provider_custom_header,
            pact_broker_url=self.pact_broker_url,
            broker_user_name=self.broker_user_name,
            broker_password=broker_password,
            provider=self.provider_pacticipant,
            consumer_api_version=f"{api_version}_production",
            git_commit_provider=self.git_commit_provider,
        )

        if failed_verify and message == "Failure! No verification processed":
            # Run against non production consumer as this could be a new version!
            failed_verify, message = self.run_pact_verifier(
                provider_base_url=self.provider_base_url,
                custom_header=self.provider_custom_header,
                pact_broker_url=self.pact_broker_url,
                broker_user_name=self.broker_user_name,
                broker_password=broker_password,
                provider=self.provider_pacticipant,
                consumer_api_version=api_version,
                git_commit_provider=self.git_commit_provider,
                provider_api_version=api_version,
            )

        if failed_verify:
            return message, failed_verify, "Failed Verification Step"

        # Canideploy with provider git_commit against latest consumer tagged with v<x>_production
        can_i_deploy, last_line = self.run_can_i_deploy(
            pact_broker_url=self.pact_broker_url,
            broker_user_name=self.broker_user_name,
            broker_password=broker_password,
            consumer_pacticipant=self.consumer_pacticipant,
            provider_pacticipant=self.provider_pacticipant,
            latest=f"{api_version}_production",
            git_commit_provider=self.git_commit_provider,
        )

        if (
            f"No version with tag {self.api_version}_production exists for {self.consumer_pacticipant}"
            in last_line
        ):
            fallback_tag = True
            # Canideploy with provider git_commit against latest consumer tagged with v<x>
            can_i_deploy, last_line = self.run_can_i_deploy(
                pact_broker_url=self.pact_broker_url,
                broker_user_name=self.broker_user_name,
                broker_password=broker_password,
                consumer_pacticipant=self.consumer_pacticipant,
                provider_pacticipant=self.provider_pacticipant,
                latest=f"{api_version}",
                git_commit_provider=self.git_commit_provider,
            )

        if (
            f"No version with tag {api_version} exists for {self.consumer_pacticipant}"
            in last_line
        ):
            message, fail_build, pact_msg = (
                "Provider Side 'Can I Deploy' Failed! No matching consumer pact!",
                True,
                last_line,
            )
        elif "No pacts or verifications have been published" in last_line:
            message, fail_build, pact_msg = (
                "Provider Side 'Can I Deploy' Failed! No pacts or verifications published!",
                True,
                last_line,
            )
        elif "failed" in last_line:
            message, fail_build, pact_msg = (
                "Provider Side 'Can I Deploy' Failed!",
                True,
                last_line,
            )
        elif "There are no missing dependencies" in last_line:
            message, fail_build, pact_msg = (
                "Provider Side 'Can I Deploy' Successful! Pact already exists and verified!",
                False,
                last_line,
            )
        elif "successful" in last_line and fallback_tag:
            message, fail_build, pact_msg = (
                "Provider Side 'Can I Deploy' Successful but against non production tag",
                False,
                last_line,
            )
        elif "successful" in last_line:
            message, fail_build, pact_msg = (
                "Provider Side 'Can I Deploy' Successful",
                False,
                last_line,
            )
        else:
            message, fail_build, pact_msg = (
                "Unknown Failure",
                can_i_deploy,
                last_line,
            )

        return message, fail_build, pact_msg

    def run_pact_verifier(
        self,
        provider_base_url,
        custom_header,
        pact_broker_url,
        broker_user_name,
        broker_password,
        provider,
        consumer_api_version,
        git_commit_provider,
        provider_api_version="None",
    ):
        command = '''{pact_path_prefix}pact/bin/pact-provider-verifier \\
            --provider-base-url=\"{provider_base_url}\" \\
            --custom-provider-header '{custom_header}' \\
            --pact-broker-base-url=\"{pact_broker_url}\" \\
            --provider=\"{provider}\" \\
            --broker-username=\"{broker_user_name}\" \\
            --broker-password=\"{broker_password}\" -r \\
            --consumer-version-tag=\"{consumer_api_version}\" \\
            --provider-app-version=\"{git_commit_provider}\"'''.format(
            provider_base_url=provider_base_url,
            custom_header=custom_header,
            pact_broker_url=pact_broker_url,
            broker_user_name=broker_user_name,
            broker_password=broker_password,
            provider=provider,
            consumer_api_version=consumer_api_version,
            git_commit_provider=git_commit_provider,
            pact_path_prefix=self.pact_path_prefix,
        )

        if provider_api_version != "None":
            command = command + f" --provider-version-tag={provider_api_version}"

        command_response = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        result_line = "0 interactions, 0 failures"

        for line in command_response.stdout.readlines():
            line = str(line)
            if "interaction" in line and "failure" in line:
                result_line = line
            pass

        clean_str = re.search(
            r"[0-9]+ interact[a-z]+, [0-9]+ fail[a-z]+|$", result_line
        ).group()

        interactions = int(re.search(r"[0-9]+", (clean_str.split(sep=", ")[0])).group())
        failures = int(re.search(r"[0-9]+", (clean_str.split(sep=", ")[1])).group())

        if interactions > 0 and failures == 0:
            failed_verify = False
            message = f"Success! {clean_str}"
        elif interactions > 0 and failures > 0:
            failed_verify = True
            message = f"Failure! {clean_str}"
        else:
            failed_verify = True
            message = "Failure! No verification processed"

        return failed_verify, message

    def run_can_i_deploy(
        self,
        pact_broker_url,
        broker_user_name,
        broker_password,
        consumer_pacticipant,
        provider_pacticipant,
        latest,
        git_commit_provider=None,
        git_commit_consumer=None,
    ):

        if git_commit_provider is None and git_commit_consumer is not None:
            command = '''{pact_path_prefix}pact/bin/pact-broker can-i-deploy \\
                --broker-base-url=\"{pact_broker_url}\" \\
                --broker-username=\"{broker_user_name}\" \\
                --broker-password=\"{broker_password}\" \\
                --pacticipant=\"{consumer_pacticipant}\" \\
                --version \"{git_commit_consumer}\" \\
                --pacticipant \"{provider_pacticipant}\" \\
                --latest \"{latest}\"'''.format(
                pact_broker_url=pact_broker_url,
                broker_user_name=broker_user_name,
                broker_password=broker_password,
                consumer_pacticipant=consumer_pacticipant,
                provider_pacticipant=provider_pacticipant,
                latest=latest,
                git_commit_consumer=git_commit_consumer,
                pact_path_prefix=self.pact_path_prefix,
            )
        elif git_commit_consumer is None and git_commit_provider is not None:
            command = '''{pact_path_prefix}pact/bin/pact-broker can-i-deploy \\
                --broker-base-url=\"{pact_broker_url}\" \\
                --broker-username=\"{broker_user_name}\" \\
                --broker-password=\"{broker_password}\" \\
                --pacticipant=\"{consumer_pacticipant}\" \\
                --latest \"{latest}\" \\
                --pacticipant \"{provider_pacticipant}\" \\
                --version \"{git_commit_provider}\"'''.format(
                pact_broker_url=pact_broker_url,
                broker_user_name=broker_user_name,
                broker_password=broker_password,
                consumer_pacticipant=consumer_pacticipant,
                provider_pacticipant=provider_pacticipant,
                latest=latest,
                git_commit_provider=git_commit_provider,
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

        return fail_build, str(last_line).replace("\\n'", "").replace("b'", "")

    @staticmethod
    def get_consumer_version(
        pact_broker_url,
        consumer_pacticipant,
        git_commit_consumer,
        broker_user_name,
        broker_password,
    ):
        # Get the API version from the tag associated with consumer commit
        full_url = f"{pact_broker_url}/pacticipants/{consumer_pacticipant}/versions/{git_commit_consumer}"
        pact_response = requests.get(full_url, auth=(broker_user_name, broker_password))

        tags = [
            tag["name"] for tag in json.loads(pact_response.text)["_embedded"]["tags"]
        ]
        if len(tags) == 0:
            tag = "Consumer has no Tags"
            success = False
        else:
            tag = sorted(tags)[0]
            success = True
        return success, tag

    @staticmethod
    def get_secret(secret_name):
        """
        Gets the secret for PACT broker
        """

        if secret_name == "local":
            return "dummy_password"

        region_name = "eu-west-1"

        client = boto3.client("sts")
        account_id = client.get_caller_identity()["Account"]
        print(account_id)

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
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret = get_secret_value_response["SecretString"]
        except exceptions.ClientError as e:
            print("Unable to get secret from Secrets Manager")
            raise e

        return secret


def main():
    parser = argparse.ArgumentParser(
        description="Check if pact contract is deployable."
    )
    parser.add_argument(
        "--provider_base_url",
        default="http://localhost:5000",
        help="Base URL of the provider (usually a mock).",
    )
    parser.add_argument(
        "--provider_custom_header",
        default="Authorization: asdf1234567890",
        help="Custom headers to include.",
    )
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
        "--consumer_pacticipant",
        default="OPGExampleApp",
        help="Name of the consumer of the API.",
    )
    parser.add_argument(
        "--provider_pacticipant",
        default="OPGExampleAPI",
        help="Name of the provider of the API.",
    )
    parser.add_argument(
        "--api_version",
        default="v1",
        help="Version of the API that you want to verify.",
    )
    parser.add_argument(
        "--git_commit_consumer",
        default="x123456",
        help="Short hash of the consumers git commit.",
    )
    parser.add_argument(
        "--git_commit_provider",
        default="z123456",
        help="Short hash of the providers git commit.",
    )

    args = parser.parse_args()
    consumer_pacticipant = urllib.parse.unquote(args.consumer_pacticipant)
    provider_pacticipant = urllib.parse.unquote(args.provider_pacticipant)
    pact_check = PactDeploymentCheck(
        args.provider_base_url,
        args.provider_custom_header,
        args.pact_broker_url,
        args.broker_user_name,
        args.broker_secret_name,
        consumer_pacticipant,
        provider_pacticipant,
        args.api_version,
        args.git_commit_consumer,
        args.git_commit_provider,
    )
    # Whether the consumer git commit is present, decides on type of check
    if args.git_commit_consumer is not None and len(args.git_commit_consumer) > 0:
        message, fail_build, pact_msg = pact_check.consumer_can_i_deploy()
    else:
        message, fail_build, pact_msg = pact_check.provider_can_i_deploy()

    print(message)
    print(pact_msg)
    if fail_build:
        exit(1)


if __name__ == "__main__":
    main()
