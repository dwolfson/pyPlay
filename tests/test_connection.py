import pytest
from src.egeria_client.utils import (
    issue_data_post,
    process_error_response,
    print_guid_list,
    get_last_guid,
    issue_post,
    issue_get,
    validate_url,
)

from src.egeria_client.connection import Connection


def test_connection():

    # connection = Connection(
    #     "active-metadata-store", "https://localhost:9443", "garygeeke", "foo"
    # )
    # print(connection.platform_url)
    # assert connection.platform_url is not None, "connection didn't work"
    assert validate_url("https://localhost.com", "connection", "server"), "invalid url"


if __name__ == "__main__":
    test_connection()
