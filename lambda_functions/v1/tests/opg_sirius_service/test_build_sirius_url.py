import validators
from .conftest import (
    test_sirius_service,
)


def test_build_sirius_url():
    url = test_sirius_service.build_sirius_url(
        "v1/api/public/lpas",
        {
            "lpa-online-tool-id": "A123567890",
        },
    )

    assert validators.url(url)


def test_build_sirius_url_with_escapable_parts():
    url = test_sirius_service.build_sirius_url(
        "path with spaces", {"complex param": "!£2 4%"}
    )

    assert validators.url(url)

    assert (
        url == "http://not-really-sirius.com/path%20with%20spaces?complex+param=%21%C2%A32+4%25"
    )
