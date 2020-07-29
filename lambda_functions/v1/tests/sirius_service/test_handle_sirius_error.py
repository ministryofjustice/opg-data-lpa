# import logging
#
# import hypothesis.strategies as st
# import pytest
# from hypothesis import given, settings
#
# from lambda_functions.v1.functions.lpa.app.api.sirius_service import handle_sirius_error
# from lambda_functions.v1.tests.sirius_service.conftest import max_examples
#
#
# @pytest.mark.parametrize(
#     "test_error_code, test_error_message, test_error_details, expected_code, "
#     "expected_message",
#     [
#         (None, None, None, 500, "Unknown error talking to Sirius, details: None"),
#         (404, None, None, 404, "Unknown error talking to Sirius, details: None"),
#         (None, "this is a message", None, 500, "this is a message, " "details: None"),
#         (
#             None,
#             None,
#             "here's some details",
#             500,
#             "Unknown error talking to Sirius, " "details: here's some details",
#         ),
#         (
#             404,
#             "this is a message",
#             "here's some details",
#             404,
#             "this is a message, " "details: here's some details",
#         ),
#     ],
# )
# def test_handle_sirius_error(
#     caplog,
#     test_error_code,
#     test_error_message,
#     test_error_details,
#     expected_code,
#     expected_message,
# ):
#
#     code, message = handle_sirius_error(
#         error_code=test_error_code,
#         error_message=test_error_message,
#         error_details=test_error_details,
#     )
#
#     assert expected_code == code
#     assert expected_message == message
#
#     with caplog.at_level(logging.ERROR):
#         assert expected_message in caplog.text
#
#
# @given(
#     test_error_code=st.integers(min_value=0),
#     test_error_message=st.text(),
#     test_error_details=st.text(),
# )
# @settings(max_examples=max_examples)
# def test_handle_sirius_error_with_hypothesis(
#     caplog, test_error_code, test_error_message, test_error_details
# ):
#
#     default_code = 500
#     default_message = "Unknown error talking to Sirius"
#     default_details = None
#
#     code, message = handle_sirius_error(
#         error_code=test_error_code,
#         error_message=test_error_message,
#         error_details=test_error_details,
#     )
#
#     if test_error_code == 0:
#         expected_code = default_code
#     else:
#         expected_code = test_error_code
#
#     expected_message = (
#         f"{test_error_message if test_error_message else default_message}, details: "
#         f"{test_error_details if test_error_details else default_details}"
#     )
#
#     assert code == expected_code
#     assert message == expected_message
#
#     with caplog.at_level(logging.ERROR):
#         assert expected_message in caplog.text
