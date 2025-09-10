from hypothesis import strategies as st
from hypothesis.provisional import domains
from yarl import URL


def url():
    """ Build http/https URL """
    scheme = st.sampled_from(["http", "https"])
    # Path must start with a slash
    pathSt = st.builds(lambda x: "/" + x, st.text())
    args = st.fixed_dictionaries(
        {
            "scheme": scheme,
            "host": domains(),
            "port": st.one_of(
                st.none(), st.integers(min_value=10, max_value=2 ** 16 - 1)
            ),
            "path": pathSt,
            "query_string": st.text(),
            "fragment": st.text(),
        }
    )
    return st.builds(lambda x: URL.build(**x), args)


def url_as_string():
    return st.builds(lambda x: str(x), url())


content_types = {
    "application": [
        "java-archive",
        "EDI-X12",
        "EDIFACT",
        "javascript",
        "octet-stream",
        "ogg",
        "pdf",
        "xhtml+xml",
        "x-shockwave-flash",
        "json",
        "ld+json",
        "xml",
        "zip",
        "x-www-form-urlencoded",
    ],
    "audio": ["mpeg", "x-ms-media"],
    "image": [
        "gif",
        "jpeg",
        "png",
        "tiff",
        "vnd.microsoft.icon",
        "x-icon",
        "vnd.djvu",
        "svg+xml",
    ],
    "multipart": ["mixed", "alternative", "related", "form-data"],
    "text": ["css", "csv", "html", "javascript", "plain", "xml"],
    "video": ["mpeg", "mp4", "quicktime", "x-ms-wmv", "x-msvideo", "x-flv", "webm"],
}


@st.composite
def content_type(draw):
    main_type_list = [x for x in content_types.keys()]

    type = draw(st.sampled_from(main_type_list))

    subtype = draw(st.sampled_from(content_types[type]))

    return f"{type}/{subtype}"
