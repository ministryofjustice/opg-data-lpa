import jwt
import pytest

from .conftest import test_sirius_service
from .strategies import content_type


def test_build_sirius_headers_content_type(patched_get_secret):
    headers = test_sirius_service._build_sirius_headers()

    assert headers["Content-Type"] == "application/json"


def test_build_sirius_headers_auth(patched_get_secret):

    headers = test_sirius_service._build_sirius_headers()
    token = headers["Authorization"].split()[1]

    try:
        jwt.decode(token.encode("UTF-8"), "this_is_a_secret_string", algorithms="HS256")
    except jwt.DecodeError as e:
        pytest.fail(f"JWT is not encoded properly: {e}")

    with pytest.raises(jwt.DecodeError):
        jwt.decode(token.encode("UTF-8"), "this_is_the_wrong_key", algorithms="HS256")
