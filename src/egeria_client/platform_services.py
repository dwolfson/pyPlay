#
# OMAG Server configuration functions.  These functions add definitions to an OMAG server's configuration document
#
import sys
from dataclasses import dataclass
from egeria_client.client import Client
from requests import Response

from egeria_client.util_exp import (
    OMAGCommonErrorCode,
    EgeriaException,
    InvalidParameterException,
)


class Platform(Client):

    """
    Client to operate Egeria Platforms

    Attributes:

        platform_url : str
            URL of the server platform to connect to
        user_id : str
            The identity of the user calling the method - this sets a default optionally used by the methods
            when the user doesn't pass the user_id on a method call.

    Methods:
        __init__(self,
                 platform_url: str,
                 end_user_id: str,
                 )
         Initializes the connection - throwing an exception if there is a problem

    """

    admin_command_root: str

    def __init__(
        self,
        server_name: str,
        platform_url: str,
        user_id: str,
        user_pwd: str = None,
        verify_flag: bool = False,
    ):
        Client.__init__(self, server_name, platform_url, user_id, user_pwd, verify_flag)
        self.admin_command_root = (
            self.platform_url
            + "/open-metadata/platform-services/users/"
            + user_id
            + "/server-platform"
        )

    def shutdown_platform(self):
        """
        Shutdown the platform.
        /open-metadata/platform-services/users/{userId}/server-platform/instance

        Parameters
        ----------

        Returns
        -------
        There is no response since the server is dead.  Also throws exceptions if no viable server or endpoint errors

        """

        url = self.admin_command_root + "/instance"
        try:
            response = self.make_request("DELETE", url)
            if response.status_code != 200:
                return response  # should never get here?
        except Exception as e:
            raise (e)

    def get_platform_origin(self) -> Response:
        """
        Get the version and origin of the platform software
        /open-metadata/platform-services/users/{userId}/server-platform/origin
        Response from this call is a string not JSON..

        Parameters
        ----------

        Returns
        -------
        Response object. Also throws exceptions if no viable server or endpoint errors

        """

        url = self.admin_command_root + "/origin"
        try:
            response = self.make_request("GET", url)
            if response.status_code != 200:
                return response  # should never get here?
            return response
        except Exception as e:
            raise (e)

    def activate_server_stored_config(self, server: str = None) -> Response:
        """
        Activate a server on the associated platform with the stored configuration.
        /open-metadata/platform-services/users/{userId}/server-platform/servers/{serverName}/instance

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response object.  Also throws exceptions if no viable server or endpoint errors

        """
        if server is None:
            server = self.server_name

        url = self.admin_command_root + "/servers/" + server + "/instance"
        try:
            response = self.make_request("POST", url)
            if response.status_code != 200:
                return response.json()  # should never get here?

            related_code = response.json().get("relatedHTTPCode")
            if related_code == 200:
                return response.json()
            else:
                class_name = sys._getframe(2).f_code.co_name
                caller_method = sys._getframe(1).f_code.co_name
                msg = OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value[
                    "message_template"
                ].format(
                    str(related_code),
                    caller_method,
                    # class_name,
                    url,
                    OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value["message_id"],
                )
                raise EgeriaException(
                    msg,
                    OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API,
                    class_name,
                    caller_method,
                    [url],
                )

        except Exception as e:
            raise (e)

    def de_activate_server(self, server: str = None) -> Response:
        """
        De-Activate a server on the associated platform.
        /open-metadata/platform-services/users/{userId}/server-platform/servers/{serverName}/instance

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response Object. Also throws exceptions if no viable server or endpoint errors

        """
        if server is None:
            server = self.server_name

        url = self.admin_command_root + "/servers/" + server + "/instance"
        try:
            response = self.make_request("DELETE", url)
            return response
        except Exception as e:
            raise (e)

    def list_servers(self) -> Response:
        """
        List all known servers on the associated platform.
        /open-metadata/platform-services/users/{userId}/server-platform/servers

        Parameters
        ----------

        Returns
        -------
        Response object. Also throws exceptions if no viable endpoint or errors

        """

        url = self.admin_command_root + "/servers"
        try:
            response = self.make_request("GET", url)
            if response.status_code != 200:
                return response.json()  # should never get here?

            related_code = response.json().get("relatedHTTPCode")
            if related_code == 200:
                return response.json()
            else:
                class_name = sys._getframe(2).f_code.co_name
                caller_method = sys._getframe(1).f_code.co_name
                msg = OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value[
                    "message_template"
                ].format(
                    str(related_code),
                    caller_method,
                    # class_name,
                    url,
                    OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value["message_id"],
                )
                raise Exception

        except InvalidParameterException as e:
            raise InvalidParameterException(
                msg,
                OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API,
                class_name,
                caller_method,
                [url],
            )

    def delete_servers(self) -> Response:
        """
        Delete all servers on the associated platform.
        /open-metadata/platform-services/users/{userId}/server-platform/servers

        Parameters
        ----------

        Returns
        -------
        Response object. Also throws exceptions if no viable endpoint or errors

        """

        url = self.admin_command_root + "/servers"
        try:
            response = self.make_request("DELETE", url)
            return response
        except Exception as e:
            raise (e)

    def get_active_configuration(self) -> Response:
        """
        Return the configuration of the server if it is running. Return invalidParameter Exception if not running.
           /open-metadata/platform-services/users/{userId}/server-platform/servers/{serverName}/instance/configuration

        Parameters
        ----------

        Returns
        -------
        Returns configuration if server is active; InvalidParameter exception thrown otherwise

        """
        msg = ""
        url = (
            self.admin_command_root
            + "/servers/"
            + self.server_name
            + "/instance/configuration"
        )

        try:
            response = self.make_request("GET", url)

            response = self.make_request("GET", url)
            if response.status_code != 200:
                return response.json()  # should never get here?

            related_code = response.json().get("relatedHTTPCode")
            if related_code == 200:
                return response.json()
            else:
                class_name = sys._getframe(2).f_code.co_name
                caller_method = sys._getframe(1).f_code.co_name
                msg = OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value[
                    "message_template"
                ].format(
                    str(related_code),
                    caller_method,
                    # class_name,
                    url,
                    OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value["message_id"],
                )
                raise Exception

        except InvalidParameterException as e:
            raise InvalidParameterException(
                msg,
                OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API,
                class_name,
                caller_method,
                [url],
            )

    def activate_server_supplied_config(
        self, config_body: str, server: str = None
    ) -> Response:
        """
        Activate a server on the associated platform with the stored configuration.
        /open-metadata/platform-services/users/{userId}/server-platform/servers/{serverName}/instance

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response object.  Also throws exceptions if no viable server or endpoint errors

        """
        if server is None:
            server = self.server_name

        url = self.admin_command_root + "/servers/" + server + "/instance/configuration"
        try:
            response = self.make_request(
                "POST",
                config_body,
                url,
            )
            return response
        except Exception as e:
            raise (e)

    def load_archive_file(self, archive_file: str, server: str = None) -> Response:
        """
        Load the server with the contents of the indicated archvie file.
        /open-metadata/platform-services/users/{userId}/server-platform/servers/{serverName}/instance/open-metadata-archives/file

        Parameters
        ----------
        archive_file: the name of the archive file to load
                - note that the path is relative to the working directory of the platform.
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response object.  Also throws exceptions if no viable server or endpoint errors

        """
        if server is None:
            server = self.server_name

        url = (
            self.admin_command_root
            + "/servers/"
            + server
            + "/instance/open-metadata-archives/file"
        )
        try:
            response = self.make_request(
                "POST",
                archive_file,
                url,
            )
            return response
        except Exception as e:
            raise (e)

    def get_active_server_status(self, server: str = None) -> Response:
        """
        Get the status for the specified server.
        /open-metadata/platform-services/users/{userId}/server-platform/servers/{server}/instance/status

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response object. Also throws exceptions if no viable endpoint or errors

        """

        url = self.admin_command_root + "/servers" + server + "/instance/status"
        try:
            response = self.make_request("GET", url)
            return response
        except Exception as e:
            raise (e)

    def is_server_known(self, server: str = None) -> Response:
        """
        Is the server known?
        /open-metadata/platform-services/users/{userId}/server-platform/servers/{server}/is-known

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response object. Also throws exceptions if no viable endpoint or errors

        """

        url = self.admin_command_root + "/servers" + server + "/is-known"
        try:
            response = self.make_request("GET", url)
            return response
        except Exception as e:
            raise (e)

    def get_active_service_list_for_server(self, server: str = None) -> Response:
        """
        List all known active servers on the associated platform.
        /open-metadata/platform-services/users/{userId}/server-platform/servers/{server}/services

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response object. Also throws exceptions if no viable endpoint or errors

        """

        url = self.admin_command_root + "/servers" + server + "/services"
        try:
            response = self.make_request("GET", url)
            return response
        except Exception as e:
            raise (e)

    def get_server_status(self, server: str = None) -> Response:
        """
        Get status of the server specified.
        /open-metadata/platform-services/users/{userId}/server-platform/servers

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response object. Also throws exceptions if no viable endpoint or errors

        """

        url = self.admin_command_root + "/servers" + server + "/status"
        try:
            response = self.make_request("GET", url)
            return response
        except Exception as e:
            raise (e)

    def get_active_server_list(self) -> Response:
        """
        List all active servers on the associated platform.
        /open-metadata/platform-services/users/{userId}/server-platform/servers/active

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        Response object. Also throws exceptions if no viable endpoint or errors

        """

        url = self.admin_command_root + "/servers/active"
        try:
            response = self.make_request("GET", url)
            return response
        except Exception as e:
            raise (e)

    def shutdown_all_servers(self) -> Response:
        """
        Shutdown all servers on the associated platform.
        /open-metadata/platform-services/users/{userId}/server-platform/servers/instance

        Parameters
        ----------

        Returns
        -------
        Response object. Also throws exceptions if no viable endpoint or errors

        """

        url = self.admin_command_root + "/servers/instance"
        try:
            response = self.make_request("DELETE", url)
            return response
        except Exception as e:
            raise (e)

    # def configurePlatformURL(self):
    #     self.admin_command_root = (
    #         self.platform_url
    #         + "/open-metadata/platform-services/users/"
    #         + self.user_id
    #         + "/server-platform"
    #     )
    #     # print("   ... configuring the platform the server will run on...")
    #     url = (
    #         self.admin_command_root
    #         + serverName
    #         + "/server-url-root?url="
    #         + serverPlatform
    #     )
    #     issuePostNoBody(url)


# def configureMaxPageSize(admin_platform_url, adminUserId, serverName, maxPageSize):
#     adminCommandURLRoot = (
#         admin_platform_url
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... configuring the maximum page size...")
#     url = adminCommandURLRoot + serverName + "/max-page-size?limit=" + maxPageSize
#     issuePostNoBody(url)
#
#
# def configureServerType(admin_platform_url, adminUserId, serverName, serverType):
#     adminCommandURLRoot = (
#         admin_platform_url
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... configuring the server's type...")
#     url = adminCommandURLRoot + serverName + "/server-type?typeName=" + serverType
#     issuePostNoBody(url)
#
#
# def clearServerType(adminPlatformURL, adminUserId, serverName):
#     adminCommandURLRoot = (
#         adminPlatformURL
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... clearing the server's type...")
#     url = adminCommandURLRoot + serverName + "/server-type?typeName="
#     issuePostNoBody(url)
#
#
# def configureOwningOrganization(
#     adminPlatformURL, adminUserId, serverName, organizationName
# ):
#     adminCommandURLRoot = (
#         adminPlatformURL
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... configuring the server's owning organization...")
#     url = (
#         adminCommandURLRoot + serverName + "/organization-name?name=" + organizationName
#     )
#     issuePostNoBody(url)
#
#
# def configureUserId(adminPlatformURL, adminUserId, serverName, userId):
#     adminCommandURLRoot = (
#         adminPlatformURL
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... configuring the server's userId...")
#     url = adminCommandURLRoot + serverName + "/server-user-id?id=" + userId
#     issuePostNoBody(url)
#
#
# def configurePassword(adminPlatformURL, adminUserId, serverName, password):
#     adminCommandURLRoot = (
#         adminPlatformURL
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... configuring the server's password (optional)...")
#     url = (
#         adminCommandURLRoot + serverName + "/server-user-password?password=" + password
#     )
#     issuePostNoBody(url)
#
#
# def configureSecurityConnection(
#     adminPlatformURL, adminUserId, serverName, securityBody
# ):
#     adminCommandURLRoot = (
#         adminPlatformURL
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... configuring the server's security connection...")
#     url = adminCommandURLRoot + serverName + "/security/connection"
#     issuePost(url, securityBody)
#
#
# def configureDefaultAuditLog(adminPlatformURL, adminUserId, serverName):
#     adminCommandURLRoot = (
#         adminPlatformURL
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... configuring the default audit log...")
#     url = adminCommandURLRoot + serverName + "/audit-log-destinations/default"
#     issuePostNoBody(url)
#
#
# def configureEventBus(adminPlatformURL, adminUserId, serverName, busBody):
#     adminCommandURLRoot = (
#         adminPlatformURL
#         + "/open-metadata/admin-services/users/"
#         + adminUserId
#         + "/servers/"
#     )
#     print("   ... configuring the event bus for this server...")
#     url = adminCommandURLRoot + serverName + "/event-bus"
#     issuePost(url, busBody)
if __name__ == "__main__":
    p = Platform("meow", "https://127.0.0.1:9443", "garygeeke", verify_flag=False)
    response = p.list_servers()
    l = response.json()["result"]
    print(l)
