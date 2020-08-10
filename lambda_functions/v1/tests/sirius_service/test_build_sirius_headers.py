import jwt
import pytest
from hypothesis import given, example

from lambda_functions.v1.tests.sirius_service.conftest import test_sirius_service
from lambda_functions.v1.tests.sirius_service.strategies import content_type


@pytest.mark.parametrize(
    "test_content_type, test_secret_key, expected_content_type",
    [
        (None, "this_is_a_secret_string", "application/json"),
        ("application/json", "this_is_a_secret_string", "application/json"),
        ("application/pdf", "this_is_a_secret_string", "application/pdf"),
    ],
)
def test_build_sirius_headers_content_type(
    test_content_type, test_secret_key, expected_content_type, patched_get_secret
):
    if test_content_type:
        headers = test_sirius_service._build_sirius_headers(
            content_type=test_content_type
        )
    else:
        headers = test_sirius_service._build_sirius_headers()

    assert headers["Content-Type"] == expected_content_type


def test_build_sirius_headers_auth(patched_get_secret):

    headers = test_sirius_service._build_sirius_headers()
    token = headers["Authorization"].split()[1]

    try:
        jwt.decode(token.encode("UTF-8"), "this_is_a_secret_string", algorithms="HS256")
    except jwt.DecodeError as e:
        pytest.fail(f"JWT is not encoded properly: {e}")

    with pytest.raises(jwt.DecodeError):
        jwt.decode(token.encode("UTF-8"), "this_is_the_wrong_key", algorithms="HS256")


@given(test_content_type=content_type())
@example(test_content_type=None)
def test_build_sirius_headers_content_type_hypothesis(
    test_content_type, patched_get_secret
):
    default_content_type = "application/json"

    headers = test_sirius_service._build_sirius_headers(content_type=test_content_type)

    if test_content_type:
        assert headers["Content-Type"] == test_content_type
    else:
        assert headers["Content-Type"] == default_content_type

        headers_no_content = test_sirius_service._build_sirius_headers()
        assert headers_no_content["Content-Type"] == default_content_type
