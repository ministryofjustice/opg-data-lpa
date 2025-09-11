from .conftest import test_sirius_service


def test_handle_sirius_error():
    code, message = test_sirius_service._handle_sirius_error(
        error_code=404,
        error_message="Page not found",
    )

    assert code == 404
    assert message == "Page not found, details: None"


def test_handle_sirius_error_with_details():
    code, message = test_sirius_service._handle_sirius_error(
        error_code=400,
        error_message="Invalid request",
        error_details={"uid": "Must be provided"},
    )

    assert code == 400
    assert message == "Invalid request, details: {'uid': 'Must be provided'}"


def test_handle_sirius_error_generic():
    code, message = test_sirius_service._handle_sirius_error()

    assert code == 500
    assert message == "Unknown error talking to Sirius, details: None"
