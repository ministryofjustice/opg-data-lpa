import jwt
import pytest

from lambda_functions.v1.functions.lpa.app.api import sirius_service

# from lambda_functions.v1.tests.sirius_service.conftest import patched_get_secret


# pytest.mark.usefixtures(patched_get_secret)
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
        headers = sirius_service.build_sirius_headers(content_type=test_content_type)
    else:
        headers = sirius_service.build_sirius_headers()

    assert headers["Content-Type"] == expected_content_type


# pytest.mark.usefixtures(patched_get_secret)
def test_build_sirius_headers_auth(patched_get_secret):

    headers = sirius_service.build_sirius_headers()
    token = headers["Authorization"].split()[1]

    try:
        jwt.decode(token.encode("UTF-8"), "this_is_a_secret_string", algorithms="HS256")
    except jwt.DecodeError as e:
        pytest.fail(f"JWT is not encoded properly: {e}")

    with pytest.raises(jwt.DecodeError):
        jwt.decode(token.encode("UTF-8"), "this_is_the_wrong_key", algorithms="HS256")
