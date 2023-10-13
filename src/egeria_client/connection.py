"""
This is a simple class to create and manage a connection to an Egeria backend

"""
from requests import ConnectTimeout
import validators

from src.egeria_client.utils import (
    issue_data_post,
    process_error_response,
    print_guid_list,
    get_last_guid,
    issue_post,
    issue_get,
    validate_url,
)


...


class Connection:
    """
    An abstract class used to hold Connected Asset Client information

    This class underlies the classes AssetConsumer and AssetOwner. The methods are used commonly by both.

    Attributes:
        server_name : str
            Name of the OMAG server to use
        server_platform_url : str
            URL of the server platform to connect to
        end_user_id : str
            The identity of the user calling the method - this sets a default optionally used by the methods
            when the user doesn't pass the user_id on a method call.
        server_user_id : str
            The identity used to connect to the server
        server_user_pwd : str
            The password used to authenticate the server identity

    Methods:
        __init__(self, server_name: str,
                 platform_url: str,
                 end_user_id: str,
                 user_id: str = None,
                 user_pwd: str = None
                 )
         Initializes the connection - throwing an exception if there is a problem



    """

    json_header = {"Content-Type": "application/json"}

    def __init__(
        self,
        server_name: str,
        server_platform_url: str,
        server_user_id: str = None,
        server_user_pwd: str = None,
    ):
        self.server_name = server_name
        self.server_platform_url = None
        self.server_user_id = server_user_id
        self.server_user_pwd = server_user_pwd

        try:
            if validate_url(server_platform_url, "Connnection", server_name):
                self.server_platform_url = server_platform_url

        except (ConnectionError, ConnectTimeout) as e:
            print(f"A connection error occurred {e}")
        except Exception as e:
            print(f"An exception occurred: {e}")


if __name__ == "__main__":
    connection = Connection(
        "active-metadata-store", "https://localhost:9443", "garygeeke", "foo"
    )
