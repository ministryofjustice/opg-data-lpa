from urllib.parse import urlparse, urlencode

# Sirius API Service
from .helpers import custom_logger

logger = custom_logger("sirius_service")



def build_sirius_url(base_url, version, endpoint, url_params=None):
    """
    Builds the url for the endpoint from variables (probably saved in env vars)

    Args:
        base_url: URL of the Sirius server
        api_route: path to public api
        endpoint: endpoint
    Returns:
        string: url
    """

    url_parts = [base_url, version, endpoint]

    sirius_url = "/".join([i for i in url_parts if i is not None])

    if url_params:
        encoded_params = urlencode(url_params)
        url = f"{sirius_url}?{encoded_params}"
    else:
        url = sirius_url

    if urlparse(url).scheme not in ["https", "http"]:
        logger.info("Unable to build Sirius URL")
        raise Exception

    return url
