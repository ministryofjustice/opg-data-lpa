import requests

import pytest
from pact_provider.check_pact_deployable import PactDeploymentCheck

provider_base_url = "http://local.mock:5000"
provider_custom_header = "Authorization: asdf1234567890"
pact_broker_url = "http://local.broker:9292"
broker_user_name = "admin"
broker_secret_name = "local"  # pactbroker_admin
consumer_pacticipant = "OPGExampleApp"
provider_pacticipant = "OPGExampleAPI"
api_version = "v1"
git_commit_consumer = "x123456"
git_commit_consumer_new = "y123456"
git_commit_provider = "a123456"
git_commit_provider_new = "b123456"
broker_password = "password"
headers = {"Content-Type": "application/json"}
file = "contract.json"
file_new = "contract_new.json"


@pytest.fixture(autouse=True)
def mock_env_setup(monkeypatch):
    monkeypatch.setenv("API_VERSION", "v1")


pact_check = PactDeploymentCheck(
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
)

pact_check_new_consumer = PactDeploymentCheck(
    provider_base_url,
    provider_custom_header,
    pact_broker_url,
    broker_user_name,
    broker_secret_name,
    consumer_pacticipant,
    provider_pacticipant,
    api_version,
    git_commit_consumer_new,
    git_commit_provider,
)

pact_check_new_provider = PactDeploymentCheck(
    provider_base_url,
    provider_custom_header,
    pact_broker_url,
    broker_user_name,
    broker_secret_name,
    consumer_pacticipant,
    provider_pacticipant,
    api_version,
    git_commit_consumer,
    git_commit_provider_new,
)


def create_pact(
    git_commit_consumer,
    provider_pacticipant,
    consumer_pacticipant,
    file,
    broker_user_name="admin",
    broker_password="password",
    headers={"Content-Type": "application/json"},
):
    full_url = f"{pact_broker_url}/pacts/provider/{provider_pacticipant}/consumer/{consumer_pacticipant}/version/{git_commit_consumer}"
    pact_response = requests.put(
        full_url,
        data=open(file, "rb"),
        auth=(broker_user_name, broker_password),
        headers=headers,
    )
    if pact_response.status_code < 399:
        return True
    else:
        return False


def delete_pact(
    consumer_pacticipant,
    provider_pacticipant,
    broker_user_name="admin",
    broker_password="password",
    headers={"Content-Type": "application/json"},
):
    full_url = f"{pact_broker_url}/pacticipants/{consumer_pacticipant}"
    pact_response = requests.delete(
        full_url, auth=(broker_user_name, broker_password), headers=headers
    )
    if pact_response.status_code < 399:
        consumer_deleted = True
    else:
        consumer_deleted = False
    full_url = f"{pact_broker_url}/pacticipants/{provider_pacticipant}"
    pact_response = requests.delete(
        full_url, auth=(broker_user_name, broker_password), headers=headers
    )
    if pact_response.status_code < 399 and consumer_deleted:
        return True
    else:
        return False


def tag_consumer_pact(
    git_commit_consumer,
    consumer_pacticipant,
    broker_user_name="admin",
    broker_password="password",
    headers={"Content-Type": "application/json"},
):
    full_url = f"{pact_broker_url}/pacticipants/{consumer_pacticipant}/versions/{git_commit_consumer}/tags/v1"
    pact_response = requests.put(
        full_url, auth=(broker_user_name, broker_password), headers=headers
    )
    if pact_response.status_code < 399:
        return True
    else:
        return False


def tag_prod_consumer_pact(
    git_commit_consumer,
    consumer_pacticipant,
    broker_user_name="admin",
    broker_password="password",
    headers={"Content-Type": "application/json"},
):
    full_url = f"{pact_broker_url}/pacticipants/{consumer_pacticipant}/versions/{git_commit_consumer}/tags/v1_production"
    pact_response = requests.put(
        full_url, auth=(broker_user_name, broker_password), headers=headers
    )
    if pact_response.status_code < 399:
        return True
    else:
        return False


def tag_prod_provider_pact(
    git_commit_provider,
    provider_pacticipant,
    broker_user_name="admin",
    broker_password="password",
    headers={"Content-Type": "application/json"},
):
    full_url = f"{pact_broker_url}/pacticipants/{provider_pacticipant}/versions/{git_commit_provider}/tags/v1_production"
    pact_response = requests.put(
        full_url, auth=(broker_user_name, broker_password), headers=headers
    )
    if pact_response.status_code < 399:
        return True
    else:
        return False


# PROVIDER SIDE WITH NO EXISTING CONSUMER
@pytest.mark.pact_test
def test_provider_no_consumer():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    message, fail_build, actual_message = pact_check.provider_can_i_deploy()
    assert message == "Failure! No verification processed"
    assert fail_build


# PROVIDER SIDE WITH CONSUMER NO TAG
@pytest.mark.pact_test
def test_provider_consumer_no_tag():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    message, fail_build, actual_message = pact_check.provider_can_i_deploy()
    assert message == "Failure! No verification processed"
    assert fail_build


# PROVIDER SIDE WITH CONSUMER WITH V1 TAG
@pytest.mark.pact_test
def test_provider_consumer_v1():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    message, fail_build, actual_message = pact_check.provider_can_i_deploy()
    assert (
        message
        == "Provider Side 'Can I Deploy' Successful but against non production tag"
    )
    assert not fail_build


# PROVIDER SIDE WITH CONSUMER WITH V1_PRODUCTION TAG
@pytest.mark.pact_test
def test_provider_consumer_v1_production():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    tag_prod_consumer_pact(git_commit_consumer, consumer_pacticipant)
    message, fail_build, actual_message = pact_check.provider_can_i_deploy()
    assert message == "Provider Side 'Can I Deploy' Successful"
    assert not fail_build


# CONSUMER SIDE WITH NO EXISTING PROVIDER
@pytest.mark.pact_test
def test_consumer_no_provider():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    message, fail_build, actual_message = pact_check.consumer_can_i_deploy()
    assert (
        message
        == "Consumer Side 'Can I Deploy' Failed! No matching provider pact with v1_production tag!"
    )
    assert fail_build


# CONSUMER SIDE V1 TAG PROVIDER SIDE V1 TAG (not possible for provider to not have tag)
@pytest.mark.pact_test
def test_consumer_v1_provider_v1():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    pact_check.provider_can_i_deploy()
    message, fail_build, actual_message = pact_check.consumer_can_i_deploy()
    assert (
        message
        == "Consumer Side 'Can I Deploy' Failed! No matching provider pact with v1_production tag!"
    )
    assert fail_build


# CONSUMER SIDE TAG V1 WITH PROVIDER TAG V1_PRODUCTION
@pytest.mark.pact_test
def test_consumer_v1_provider_v1_production():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    pact_check.provider_can_i_deploy()
    tag_prod_provider_pact(git_commit_provider, provider_pacticipant)
    message, fail_build, actual_message = pact_check.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Successful"
    assert not fail_build


# CONSUMER SIDE CREATES WORKING PACT THEN CHANGES PACT SPEC
@pytest.mark.pact_test
def test_working_to_broken():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    pact_check.provider_can_i_deploy()
    tag_prod_provider_pact(git_commit_provider, provider_pacticipant)
    message, fail_build, actual_message = pact_check.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Successful"
    assert not fail_build
    create_pact(
        git_commit_consumer_new, provider_pacticipant, consumer_pacticipant, file_new
    )
    tag_consumer_pact(git_commit_consumer_new, consumer_pacticipant)
    (
        message,
        fail_build,
        actual_message,
    ) = pact_check_new_consumer.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Failed!"
    assert (
        actual_message
        == "The verification between version y123456 of OPGExampleApp and the latest version of OPGExampleAPI with tag v1_production (a123456) failed"
    )


# CONSUMER CREATES WORKING PACT THEN COMMITS SAME PACT SPEC
@pytest.mark.pact_test
def test_repush_same_pact():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    pact_check.provider_can_i_deploy()
    tag_prod_provider_pact(git_commit_provider, provider_pacticipant)
    message, fail_build, actual_message = pact_check.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Successful"
    assert not fail_build
    create_pact(
        git_commit_consumer_new, provider_pacticipant, consumer_pacticipant, file
    )
    tag_consumer_pact(git_commit_consumer_new, consumer_pacticipant)
    (
        message,
        fail_build,
        actual_message,
    ) = pact_check_new_consumer.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Successful"
    assert (
        actual_message
        == "All required verification results are published and successful"
    )


# CONSUMER CREATES NON WORKING PACT THEN WORKING PACT THEN PROVIDER TRIES TO DEPLOY
@pytest.mark.pact_test
def test_latest_working_pact():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(
        git_commit_consumer, provider_pacticipant, consumer_pacticipant, file_new
    )
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    pact_check.provider_can_i_deploy()
    tag_prod_provider_pact(git_commit_provider, provider_pacticipant)
    message, fail_build, actual_message = pact_check.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Failed!"
    create_pact(
        git_commit_consumer_new, provider_pacticipant, consumer_pacticipant, file
    )
    tag_consumer_pact(git_commit_consumer_new, consumer_pacticipant)
    (
        message,
        fail_build,
        actual_message,
    ) = pact_check_new_consumer.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Successful"
    assert (
        actual_message
        == "All required verification results are published and successful"
    )
    (
        message,
        fail_build,
        actual_message,
    ) = pact_check_new_provider.provider_can_i_deploy()
    assert (
        message
        == "Provider Side 'Can I Deploy' Successful but against non production tag"
    )
    assert (
        actual_message
        == "All required verification results are published and successful"
    )


# CONSUMER CREATES WORKING PACT THEN NON WORKING THEN PROVIDER TRIES TO DEPLOY
@pytest.mark.pact_test
def test_latest_broken_pact():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    pact_check.provider_can_i_deploy()
    tag_prod_provider_pact(git_commit_provider, provider_pacticipant)
    message, fail_build, actual_message = pact_check.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Successful"
    create_pact(
        git_commit_consumer_new, provider_pacticipant, consumer_pacticipant, file_new
    )
    tag_consumer_pact(git_commit_consumer_new, consumer_pacticipant)
    (
        message,
        fail_build,
        actual_message,
    ) = pact_check_new_consumer.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Failed!"
    message, fail_build, actual_message = pact_check.provider_can_i_deploy()
    assert message == "Failure! 1 interaction, 1 failure"
    assert actual_message == "Failed Verification Step"


# CONSUMER CREATES WORKING PACT IN PROD BUT NON WORKING IN BRANCH THEN PROVIDER TRIES TO DEPLOY
@pytest.mark.pact_test
def test_old_working_prod_pact():
    delete_pact(consumer_pacticipant, provider_pacticipant)
    create_pact(git_commit_consumer, provider_pacticipant, consumer_pacticipant, file)
    tag_consumer_pact(git_commit_consumer, consumer_pacticipant)
    pact_check.provider_can_i_deploy()
    tag_prod_provider_pact(git_commit_provider, provider_pacticipant)
    message, fail_build, actual_message = pact_check.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Successful"
    tag_prod_consumer_pact(git_commit_consumer, consumer_pacticipant)
    create_pact(
        git_commit_consumer_new, provider_pacticipant, consumer_pacticipant, file_new
    )
    tag_consumer_pact(git_commit_consumer_new, consumer_pacticipant)
    (
        message,
        fail_build,
        actual_message,
    ) = pact_check_new_consumer.consumer_can_i_deploy()
    assert message == "Consumer Side 'Can I Deploy' Failed!"
    message, fail_build, actual_message = pact_check.provider_can_i_deploy()
    assert message == "Provider Side 'Can I Deploy' Successful"
    assert (
        actual_message
        == "All required verification results are published and successful"
    )
