#
# OMAG Server configuration functions.  These functions add definitions to an OMAG server's configuration document
#
from dataclasses import dataclass
from egeria_client.client import Client


class Platform(Client):

    """
    Client to administer Egeria Platforms

    Attributes:

        admin_platform_url : str
            URL of the server platform to connect to
        end_user_id : str
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
    def __init__(self,
                 server_name:str ,
                 platform_url: str,
                 user_id: str,
                 user_pwd:str = None,
                 verify_flag: bool = False
                 ):
        Client.__init__(
            self,
            server_name,
            platform_url,
            user_id,
            user_pwd,
            verify_flag
        )
        self.admin_command_root = (self.platform_url +
            "/open-metadata/platform-services/users/" +
            user_id +
            "/server-platform")


    def activate_server(self, server: str = None) -> bool:
        """
        Activate a server on the associated platform.

        Parameters
        ----------
        server : Use the server if specified. If None, use the default server associated with the Platform object.

        Returns
        -------
        True if successful, False if not. Also throws exceptions if no viable server or endpoint errors

        """
        if server is None:
            server = self.server_name
        /open-metadata/platform-services/users/{userId}/server-platform/servers/{serverName}/instance
        url = (
            self.admin_command_root
            + "/servers/"
            + server
            + "/
        )
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


def configureMaxPageSize(admin_platform_url, adminUserId, serverName, maxPageSize):
    adminCommandURLRoot = (
        admin_platform_url
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... configuring the maximum page size...")
    url = adminCommandURLRoot + serverName + "/max-page-size?limit=" + maxPageSize
    issuePostNoBody(url)


def configureServerType(admin_platform_url, adminUserId, serverName, serverType):
    adminCommandURLRoot = (
        admin_platform_url
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... configuring the server's type...")
    url = adminCommandURLRoot + serverName + "/server-type?typeName=" + serverType
    issuePostNoBody(url)


def clearServerType(adminPlatformURL, adminUserId, serverName):
    adminCommandURLRoot = (
        adminPlatformURL
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... clearing the server's type...")
    url = adminCommandURLRoot + serverName + "/server-type?typeName="
    issuePostNoBody(url)


def configureOwningOrganization(
    adminPlatformURL, adminUserId, serverName, organizationName
):
    adminCommandURLRoot = (
        adminPlatformURL
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... configuring the server's owning organization...")
    url = (
        adminCommandURLRoot + serverName + "/organization-name?name=" + organizationName
    )
    issuePostNoBody(url)


def configureUserId(adminPlatformURL, adminUserId, serverName, userId):
    adminCommandURLRoot = (
        adminPlatformURL
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... configuring the server's userId...")
    url = adminCommandURLRoot + serverName + "/server-user-id?id=" + userId
    issuePostNoBody(url)


def configurePassword(adminPlatformURL, adminUserId, serverName, password):
    adminCommandURLRoot = (
        adminPlatformURL
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... configuring the server's password (optional)...")
    url = (
        adminCommandURLRoot + serverName + "/server-user-password?password=" + password
    )
    issuePostNoBody(url)


def configureSecurityConnection(
    adminPlatformURL, adminUserId, serverName, securityBody
):
    adminCommandURLRoot = (
        adminPlatformURL
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... configuring the server's security connection...")
    url = adminCommandURLRoot + serverName + "/security/connection"
    issuePost(url, securityBody)


def configureDefaultAuditLog(adminPlatformURL, adminUserId, serverName):
    adminCommandURLRoot = (
        adminPlatformURL
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... configuring the default audit log...")
    url = adminCommandURLRoot + serverName + "/audit-log-destinations/default"
    issuePostNoBody(url)


def configureEventBus(adminPlatformURL, adminUserId, serverName, busBody):
    adminCommandURLRoot = (
        adminPlatformURL
        + "/open-metadata/admin-services/users/"
        + adminUserId
        + "/servers/"
    )
    print("   ... configuring the event bus for this server...")
    url = adminCommandURLRoot + serverName + "/event-bus"
    issuePost(url, busBody)
