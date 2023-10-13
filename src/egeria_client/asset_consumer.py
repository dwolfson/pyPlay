# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
#
#
# Asset Consumer OMAS
#
import requests

from src.egeria_client.assetLib import (
    print_asset_comment_replies,
    print_related_assets,
    print_asset_comments,
    Comment,
    Asset,
    AssetUniverse,
)
from src.egeria_client.util_exp import (
    issue_data_post,
    process_error_response,
    print_guid_list,
    get_last_guid,
    issue_post,
    issue_get,
    validate_url,
)

# from src.egeria_client.utils import issue_data_post, process_error_response, print_guid_list, \
#     get_last_guid, issue_post, issue_get, validate_url, Asset
from src.egeria_client.utils import comment_types, star_ratings
import json


def print_comment_list(comment_list: [Comment]):
    """Print all the comments in the comment_list

    Parameters
        comment_list: [Comment]
            A list of comment objects
    """

    for x in comment_list:
        print(x)
    print("\n")


class ConnectedAssetClientBase:
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
        get_asset_properties (asset_guid)
            returns the properties for the asset

        get_asset_summary (asset_guid)
            returns a summary of asset information

        get_comments (asset_guid, extended_properties - optional, debug - optional, start_from - optional,
                      page_size - optional, end_user_id - optional, service_marker - optional)
                Returns all top level comments linked to the specified asset in a list of comment objects

        get_comment_replies (asset_guid, comment_guid, extended_properties - optional, debug - optional,
                            start_from - optional, page_size - optional, end_user_id - optional,
                            service_marker - optional)
                Returns all replies for the specified comment_guid in a list of comment objects

        get_certifications (asset_guid, extended_properties - optional, debug - optional, start_from - optional,
                            page_size - optional, end_user_id - optional, service_marker - optional)
                Returns certifications associated with the specified asset_guid as a list of certification objects

    """

    json_header = {"Content-Type": "application/json"}

    def __init__(
        self,
        server_name: str,
        server_platform_url: str,
        end_user_id: str,
        server_user_id: str = None,
        server_user_pwd: str = None,
    ):

        if validate_url(server_platform_url, "ConnectedAssetClientBase", "server?"):
            self.server_platform_url = server_platform_url

        self.guids = None
        self.server_name = server_name
        self.server_user_id = server_user_id
        self.server_user_pwd = server_user_pwd

        self.end_user_id = end_user_id

    def get_asset_properties(self, asset_guid: str):
        pass

    def get_asset_summary(self, asset_guid: str, method_name: str) -> Asset:
        pass

    def get_comments(
        self,
        asset_guid: str,
        extended_properties=None,
        debug: bool = False,
        start_from: int = 0,
        page_size: int = 0,
        end_user_id: str = None,
        service_marker: str = "asset-consumer",
    ):
        """
        Parameters
        ----------
        asset_guid :
        extended_properties :
        debug :
        start_from :
        page_size :
        end_user_id :
        service_marker :

        Returns
        -------

        """
        comment_list = []
        if end_user_id is None:
            end_user_id = self.end_user_id

        connected_asset_url = (
            self.server_platform_url
            + "/servers/"
            + self.server_name
            + "/open-metadata/common-services/"
            + service_marker
            + "/connected-asset/users/"
            + end_user_id
        )

        comment_query_url = (
            connected_asset_url
            + "/assets/"
            + asset_guid
            + "/comments?elementStart="
            + str(start_from)
            + "&maxElements="
            + str(page_size)
        )

        response = requests.get(
            comment_query_url, verify=False, headers=self.json_header
        )

        if response.status_code != 200:
            raise ConnectionError(response.text)

        response_objects = response.json().get("list")

        if response_objects:
            for x in range(len(response_objects)):
                comment_list.append(Comment(response_objects[x]))
            if debug:
                print(f"In {__name__} the comments were returned")
            return comment_list
        elif debug:
            print(
                "In get_comments, no comments returned, response was {response.json()}"
            )
            return None

    def get_comment_replies(
        self,
        asset_guid: str,
        comment_guid: str,
        extended_properties=None,
        debug: bool = False,
        end_user_id: str = None,
        service_marker: str = "asset-consumer",
    ):
        comment_list = []
        if end_user_id is None:
            end_user_id = self.end_user_id

        connectedAssetURL = (
            self.server_platform_url
            + "/servers/"
            + self.server_name
            + "/open-metadata/common-services/"
            + service_marker
            + "/connected-asset/users/"
            + end_user_id
        )

        comment_query = (
            connectedAssetURL
            + "/assets/"
            + asset_guid
            + "/comments/"
            + comment_guid
            + "/replies?elementStart=0&maxElements=50"
        )
        response = issue_get(comment_query)
        response_objects = response.json().get("list")
        if response_objects:
            for x in response_objects:
                if x:
                    comment_list.append(Comment(x))
            if debug:
                print(f"in get_comment_replies there are {len(comment_list)} replies")
                print(f"replies found in get_comment_replies are {comment_list}")
            return comment_list
        elif debug:
            print("In get_comment_replies, No comments returned")
            return None

    # asset universe?
    def get_certifications(
        self,
        asset_guid: str,
        extended_properties=None,
        debug: bool = False,
        start_from: int = 0,
        page_size: int = 0,
        end_user_id: str = None,
        service_marker: str = "asset-consumer",
    ):
        pass


class AssetConsumer(ConnectedAssetClientBase):
    """AssetConsumer provides users the ability to find, retrieve information and annotate assets

    Attributes
    ----------
    server_name: str
        the name of the server we want to connect to - the server runs on a
    server_platform: str
        the name of the server platform the server is running in
    server_platform_url: str
        the url of the server platform
    user_id: str
        the user id of the individual we are making the request on behalf of
    guids: str[]
        a list of GUIDs
    asset_consumer_endpoint: str
        constructed string representing the base endpoint URL

    Methods
    -------
    get_assets_by_meaning (term_guid, debug: bool = False, end_user_id: str = None, extended_properties=None,
                           start_from: int = 0, page_size: int = 0) -> list[str]
        returns assets associated with the specified term_guid as a list of asset_guids

    find_meanings (term: str, end_user_id: str = None, extended_properties=None, debug: bool = False,
                   start_from: int = 0, page_size: int = 0) -> list[str]
        returns the assets associated with the specified glossary term as a list of guids

    find_assets(search_string: str)
        searches for assets matching the regular expression in the search_string

    add_comment_to_asset(asset_guid, comment_text, comment_type, is_public)
        adds the comment_text as a comment to the asset represented by asset_guid

    add_reply_to_asset_comment(asset_guid, comment_guid, comment_text, comment_type, is_public)
        adds a reply to the comment represented by comment_guid on asset asset_guid
    remove_comment_from_asset()  <--

    asset_consumer_get_asset_universe(asset_guid)
        returns the universe of information about the asset specified by asset_guid

    asset_consumer_print_asset_comment_replies(asset_guid, comment_guid)
        prints replies to an asset comment specified by comment_guid

    asset_consumer_print_related_assets(asset_guid)

    asset_consumer_print_asset_universe(asset_guid)

    asset_consumer_print_asset_comments(asset_guid)


    """

    def __init__(
        self,
        server_name: str,
        server_platform_url: str,
        end_user_id: str,
        server_user_id: str = None,
        server_user_pwd: str = None,
    ):
        """This constructor takes connection information to instantiate an AssetConsumer object"""
        ConnectedAssetClientBase.__init__(
            self,
            server_name,
            server_platform_url,
            end_user_id,
            server_user_id,
            server_user_pwd,
        )
        self.asset_consumer_endpoint = "{0}/servers/{1}/open-metadata/access-services/asset-consumer/users/".format(
            server_platform_url, server_name
        )

    def get_assets_by_meaning(
        self,
        term_guid,
        debug: bool = False,
        end_user_id: str = None,
        extended_properties=None,
        start_from: int = 0,
        page_size: int = 0,
    ) -> list[str]:
        """Returns assets associated with the specified term_guid as a list of asset_guids

        Parameters
        ----------
        term_guid : str
            GUID identifier for the glossary term of interest

        Returns
        -------
            list[str] - a list of asset_guids represented as strings


        Other Parameters
        ----------------
        end_user_id : str = none, optional
            the identity of the end user. Default is none. If not specified (or none) end_user_id is set to
            the default defined in the constructor
        extended_properties : optional
        debug : bool = False, optional
            Set False by default, if True then debug print statements will be issued in the method
        start_from : str = 0, optional
            Specifies the starting page when iterating through multiple pages of results
            Defaults to 0 if not explicitly set
        page_size : str = 0, optional
            Specifies the number of elements to return in an iteration.
            Defaults to 0 which uses the server default page size

        """
        if end_user_id is None:
            end_user_id = self.end_user_id

        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

        return response

    def find_meanings(
        self,
        term: str,
        end_user_id: str = None,
        extended_properties=None,
        debug: bool = False,
        start_from: int = 0,
        page_size: int = 0,
    ) -> [str]:
        """Returns the assets associated with the specified glossary term as a list of guids
        Parameters
        ----------
        term : str
            the glossary term we are investigating for related assets

        Returns
        -------
            List of asset_guid strings

        Other Parameters
        ----------------
        end_user_id : str = none, optional
            the identity of the end user. Default is none. If not specified (or none) end_user_id is set to
            the default defined in the constructor
        extended_properties : optional
        debug : bool = False, optional
            Set False by default, if True then debug print statements will be issued in the method.
        start_from : str = 0, optional
            Specifies the starting page when iterating through multiple pages of results.
            Defaults to 0 if not explicitly set
        page_size : str = 0, optional
            Specifies the number of elements to return in an iteration.
            Defaults to 0 which uses the server default page size.
        """
        if end_user_id is None:
            end_user_id = self.end_user_id

        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    def find_assets(
        self,
        search_string: str,
        extended_properties=None,
        debug: bool = False,
        start_from: int = 0,
        page_size: int = 0,
        end_user_id: str = None,
    ) -> [str]:
        """Searches for assets matching the regular expression in the search_string
        Parameters
        ----------
        search_string : a regular expression string defining the search criteria

        Returns
        -------
        Returns a list of the asset guids found as a list of strings

        Other Parameters
        ----------------
        end_user_id : str = none, optional
            the identity of the end user. Default is none. If not specified (or none) end_user_id is set to
            the default defined in the constructor
        extended_properties : optional
        debug : bool = False, optional
            Set False by default, if True then debug print statements will be issued in the method.
        start_from : str = 0, optional
            Specifies the starting page when iterating through multiple pages of results.
            Defaults to 0 if not explicitly set
        page_size : str = 0, optional
            Specifies the number of elements to return in an iteration.
            Defaults to 0 which uses the server default page size.

        Raises
        ------
            ConnectionError
        """
        guids = None

        if end_user_id is None:
            end_user_id = self.end_user_id

        asset_consumer_url = (
            self.server_platform_url
            + "/servers/"
            + self.server_name
            + "/open-metadata/access-services/asset-consumer/users/"
            + end_user_id
        )

        body = {"class": "SearchStringRequestBody", "searchString": search_string}

        url = (
            asset_consumer_url
            + "/assets/by-search-string?startFrom="
            + str(start_from)
            + "&pageSize="
            + str(page_size)
        )
        response = requests.post(url, json=body, verify=False, headers=self.json_header)

        if debug:
            print(f"In find_assets response is {response.json()}")

        if response.status_code != 200:
            raise ConnectionError(response.text)

        guids = response.json().get("guids")
        return guids

    def get_asset_properties(
        self, asset_guid: str, end_user_id: str = None, extended_properties=None
    ):
        """Returns the properties for the asset
        Parameters
        ----------
        asset_guid :
        end_user_id :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id

        asset_consumer_url = (
            self.server_platform_url
            + "/servers/"
            + self.server_name
            + "/open-metadata/access-services/asset-consumer/users/"
            + end_user_id
        )
        body = {"class": "SearchStringRequestBody", "searchString": search_string}

        url = (
            asset_consumer_url
            + "/assets/by-search-string?startFrom="
            + str(start_from)
            + "&pageSize="
            + str(page_size)
        )
        response = requests.post(url, json=body, verify=False, headers=self.json_header)

        if debug:
            print(f"In find_assets response is {response.json()}")

        if response.status_code != 200:
            raise ConnectionError(response.text)

        guids = response.json().get("guids")
        return guids

    # returns list of Meaning Elements
    def get_meaning_by_name(
        self,
        term: str,
        end_user_id: str = None,
        extended_properties=None,
        debug: bool = False,
        start_from: int = 0,
        page_size: int = 0,
    ):
        """
        Parameters
        ----------
        term :
        end_user_id :
        extended_properties :
        debug :
        start_from :
        page_size :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        asset_consumer_url = (
            self.server_platform_url
            + "/servers/"
            + self.server_name
            + "/open-metadata/access-services/asset-consumer/users/"
            + end_user_id
        )

        body = {"class": "NameRequestBody", "name": term}

        url = (
            asset_consumer_url
            + "/meanings/by-name?startFrom"
            + str(start_from)
            + "&pageSize="
            + str(page_size)
        )
        response = requests.post(url, json=body, verify=False, headers=self.json_header)

        if debug:
            print(f"In find_assets response is {response.json()}")

        if response.status_code != 200:
            raise ConnectionError(response.text)

    # Look at this more closely
    # guids = response.json().get('guids')

    # return (guids)

    # returns meaning Element
    def get_meaning(
        self, term_guid: str, end_user_id: str = None, extended_properties=None
    ):
        """
        Parameters
        ----------
        term_guid :
        end_user_id :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        asset_consumer_url = (
            self.server_platform_url
            + "/servers/"
            + self.server_name
            + "/open-metadata/access-services/asset-consumer/users/"
            + end_user_id
        )

        url = asset_consumer_url + "/meanings/" + term_guid
        response = requests.get(url, verify=False, headers=self.json_header)

        if debug:
            print(f"In find_assets response is {response.json()}")

        if response.status_code != 200:
            raise ConnectionError(response.text)

        # guids = response.json().get('guids')
        # create a meaning object to return
        return

    #
    # Comments

    def add_comment_to_asset(
        self,
        asset_guid: str,
        comment_text: str,
        comment_type: str,
        is_public: bool,
        extended_properties: object = None,
        debug: bool = False,
        end_user_id: str = None,
    ) -> str:
        """
        Parameters
        ----------
        asset_guid : str
            Unique identifier of the asset we are adding a comment to
        comment_text : str
            Text of the comment to add
        comment_type : str
            Comment type from the comment_type enum list
        is_public : bool
            If true, then the comment is visible to all that are allowed to see the asset

        Other Parameters
        ----------------
        end_user_id : str = none, optional
            the identity of the end user. Default is none. If not specified (or none) end_user_id is set to
            the default defined in the constructor
        extended_properties : optional
        debug : bool = False, optional
            Set False by default, if True then debug print statements will be issued in the method.

        Returns
        -------
          str - if successful, the guid of newly added comment
          None - if unsuccessful

        Raises
        ------
            ConnectionError (fix this) <--
        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        if comment_type not in comment_types:
            raise ValueError(comment_type + " is an Invalid comment type")
        if is_public:
            json_public = "true"
        else:
            json_public = "false"

        add_comment_url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/comments"
        )
        comment_body = {
            "class": "CommentRequestBody",
            "commentType": comment_type,
            "commentText": comment_text,
            "isPublic": json_public,
        }
        response = requests.post(
            add_comment_url, json=comment_body, verify=False, headers=self.json_header
        )

        if response.status_code != 200:
            raise ConnectionError(response.text)

        comment_guid = response.json().get("guid")
        if comment_guid:
            return comment_guid
        elif debug:
            print(
                f"In add_comment - not comment guid found, response is {response.json()}"
            )
            return None

    def update_comment(
        self,
        asset_guid: str,
        comment_guid: str,
        comment_text: str,
        comment_type: str,
        is_public: bool,
        end_user_id: str = None,
        extended_properties=None,
        debug: bool = False,
    ):
        """
        Parameters
        ----------
        asset_guid : str
            Unique identifier of the asset we are updating the comment of
        comment_guid : str
            Unique identifier of the comment we are updating
        comment_text : str
            Text of the comment to add
        comment_type : str
            Comment type from the comment_type enum list
        is_public : bool
            If true, then the comment is visible to all that are allowed to see the asset

        Other Parameters
        ----------------
        end_user_id : str = none, optional
            the identity of the end user. Default is none. If not specified (or none) end_user_id is set to
            the default defined in the constructor
        extended_properties : optional
        debug : bool = False, optional
            Set False by default, if True then debug print statements will be issued in the method.

        Returns
        -------
            No return value
        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        if comment_type not in comment_types:
            raise ValueError(comment_type + " is an Invalid comment type")
        if is_public:
            json_public = "true"
        else:
            json_public = "false"

        update_comment_url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/comments/"
            + comment_guid
            + "/update"
        )
        comment_body = {
            "class": "CommentRequestBody",
            "commentType": comment_type,
            "commentText": comment_text,
            "isPublic": json_public,
        }
        response = requests.post(
            update_comment_url,
            json=comment_body,
            verify=False,
            headers=self.json_header,
        )

        if response.status_code != 200:
            raise ConnectionError(response.text)
        elif debug:
            print(f"update_comment worked: {response.text}")
        return

    def remove_comment(
        self,
        asset_guid: str,
        comment_guid: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid : str
            Unique identifier of the asset we are updating the comment of
        comment_guid : str
            Unique identifier of the comment we are updating
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/comments/"
            + comment_guid
            + "/delete"
        )
        body = {
            "class": "NullRequestBody",
        }

        if debug:
            print(f" Comment to delete is: {comment_guid}")

        response = requests.post(url, json=body, verify=False, headers=self.json_header)

        if response.status_code != 200:
            raise ConnectionError(response.text)
        elif debug:
            print(f"in remove_comment, response is: {response.json()}")
        return

    def add_comment_reply(
        self,
        asset_guid: str,
        comment_guid: str,
        comment_text: str,
        comment_type: str,
        is_public: bool,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid :
        comment_guid :
        comment_text :
        comment_type :
        is_public :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        if comment_type not in comment_types:
            raise ValueError(comment_type + " is an Invalid comment type")
        if is_public:
            json_public = "true"
        else:
            json_public = "false"
        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/comments/"
            + comment_guid
            + "/replies"
        )

        body = {
            "class": "CommentRequestBody",
            "commentType": comment_type,
            "commentText": comment_text,
            "isPublic": json_public,
        }
        response = requests.post(url, json=body, verify=False, headers=self.json_header)

        if response.status_code != 200:
            raise ConnectionError(response.text)

        comment_guid = response.json().get("guid")
        if comment_guid:
            return comment_guid
        elif debug:
            print(
                f"No reply added to comment {comment_guid} with response of {response.text}"
            )
            return None

    #
    # Likes & Ratings
    #

    def add_like(
        self,
        asset_guid: str,
        is_public: bool,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid :
        is_public :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        if is_public:
            json_public = "true"
        else:
            json_public = "false"

        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/likes"
        )
        body = {"isPublic": json_public}
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response.text}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        return True

    def remove_like(
        self,
        asset_guid: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id

        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/likes/delete"
        )
        body = {"isPublic": json_public}
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        return True

    def add_rating(
        self,
        asset_guid: str,
        star_rating: str,
        review: str,
        is_public: bool,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid :
        star_rating :
        review :
        is_public :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        if star_rating not in star_ratings:
            raise ValueError(star_rating + " is an Invalid rating")
        if is_public:
            json_public = "true"
        else:
            json_public = "false"
        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/ratings"
        )
        body = {
            "starRating": star_rating,
            "review": review,
            "user": end_user_id,
            "isPublic": json_public,
        }
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response.text}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        return True

    def remove_rating(
        self,
        asset_guid: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/ratings/delete"
        )
        body = {}
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response.text}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        return True

    #
    # Tags
    #
    def add_tag(
        self,
        asset_guid: str,
        tag_guid: str,
        is_public: bool,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid :
        tag_guid :
        is_public :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        if is_public:
            json_public = "true"
        else:
            json_public = "false"
        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/tags/"
            + tag_guid
        )
        body = {"isPublic": json_public}

        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response.text}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        return

    def add_tag_to_element(
        self,
        element_guid: str,
        tag_guid: str,
        is_public: bool,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        element_guid :
        tag_guid :
        is_public :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        if is_public:
            json_public = "true"
        else:
            json_public = "false"

        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/assets/"
            + asset_guid
            + "/elements/"
            + element_guid
            + "/tags/"
            + tag_guid
        )
        body = {"isPublic": json_public}

        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        return True

    def create_private_tag(
        self,
        tag_name: str,
        tag_description: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        tag_name :
        tag_description :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id

        url = self.asset_consumer_endpoint + end_user_id + "/tags"
        body = {
            "isPublic": "false",
            "isPrivateTag": "true",
            "name": tag_name,
            "description": tag_description,
            "user": end_user_id,
        }
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response.text}")

        if response.status_code != 200:
            raise ConnectionError(response.text)

        return response.json().get("guid")

    def create_public_tag(
        self,
        tag_name: str,
        tag_description: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        tag_name :
        tag_description :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id

        url = self.asset_consumer_endpoint + end_user_id + "/tags"
        body = {
            "isPublic": "true",
            "isPrivateTag": "false",
            "name": tag_name,
            "description": tag_description,
            "user": end_user_id,
        }
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        return response.json().get("guid")

    def delete_tag(
        self,
        tag_guid,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        tag_guid :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        url = (
            self.asset_consumer_endpoint + end_user_id + "/tags" + tag_guid + "/delete"
        )
        body = {
            "class": "NullRequestBody",
        }
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response.text}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        else:
            return True

    def find_my_tags(
        self,
        tag: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
        start_from: int = 0,
        page_size: int = 0,
    ):
        """
        Parameters
        ----------
        tag :
        end_user_id :
        debug :
        extended_properties :
        start_from :
        page_size :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        url = (
            self.asset_consumer_endpoint
            + end_user_id
            + "/tags/private/by-search-string/?startFrom"
            + str(start_from)
            + "&pageSize="
            + str(page_size)
        )

        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response.text}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    def find_tags(
        self,
        tag: str,
        end_user_id: str = None,
        extended_properties=None,
        debug: bool = False,
        start_from: int = 0,
        page_size: int = 0,
    ):
        """
        Parameters
        ----------
        tag :
        end_user_id :
        extended_properties :
        debug :
        start_from :
        page_size :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        url = self.asset_consumer_endpoint + end_user_id + "/tags/by-search-string"
        body = {"tag": tag}
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        return response.content

    # returns informalTagElement
    def get_tag(
        self,
        tag_guid: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        tag_guid :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    # returns list of informatlTagElement
    def get_tags_by_name(
        self,
        tag: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
        start_from: int = 0,
        page_size: int = 0,
    ):
        """
        Parameters
        ----------
        tag :
        end_user_id :
        debug :
        extended_properties :
        start_from :
        page_size :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id

        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    def get_assets_by_tag(
        self,
        tag_guid: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
        start_from: str = "0",
        page_size: str = "40",
    ):
        """
        Parameters
        ----------
        tag_guid :
        end_user_id :
        debug :
        extended_properties :
        start_from :
        page_size :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    # returns list of informatlTagElement
    def get_my_tags_by_name(
        self,
        tag: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
        start_from: int = 0,
        page_size: int = 0,
    ):
        """
        Parameters
        ----------
        tag :
        end_user_id :
        debug :
        extended_properties :
        start_from :
        page_size :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    def remove_tag(
        self,
        asset_guid: str,
        tag_guid,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid :
        tag_guid :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    def remove_tag_from_element(
        self,
        asset_guid: str,
        element_guid: str,
        tag_guid: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        asset_guid :
        element_guid :
        tag_guid :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    def update_tag_description(
        self,
        tag_guid: str,
        tag_description: str,
        end_user_id: str = None,
        debug: bool = False,
        extended_properties=None,
    ):
        """
        Parameters
        ----------
        tag_guid :
        tag_description :
        end_user_id :
        debug :
        extended_properties :

        Returns
        -------

        """
        if end_user_id is None:
            end_user_id = self.end_user_id
        response = requests.post(url, json=body, verify=False, headers=self.json_header)
        if debug:
            print(f"response is: {response}")
        if response.status_code != 200:
            raise ConnectionError(response.text)

    def print_asset_guids(self, search_string):
        """
        Parameters
        ----------
        search_string :

        Returns
        -------

        """
        guids = self.find_assets(search_string)
        if guids:
            print_guid_list(guids)

    # def asset_consumer_get_asset_universe(self, asset_guid):
    #     return get_asset_universe(self.server_name, self.server_platform_name, self.platform_url,
    #                               "asset-consumer", self.user_id, asset_guid)

    # def asset_consumer_print_asset_universe(self, asset_guid):
    #     print_asset_universe(self.server_name, self.server_platform_name, self.platform_url, "asset-consumer",
    #                          self.user_id, asset_guid)

    def print_asset_comment_replies(self, asset_guid, comment_guid):
        print_asset_comment_replies(
            self.server_name,
            "FIXME",
            self.server_platform_url,
            "asset-consumer",
            self.end_user_id,
            asset_guid,
            comment_guid,
        )

    def print_related_assets(self, asset_guid):
        print_related_assets(
            self.server_name,
            "fixme",
            self.server_platform_url,
            "asset-consumer",
            self.end_user_id,
            asset_guid,
        )

    def print_comments(self, asset_guid: object) -> object:
        print_asset_comments(
            self.server_name,
            "fixme",
            self.server_platform_url,
            "asset-consumer",
            self.end_user_id,
            asset_guid,
        )


class AssetUniverse:
    """This class holds the asset universe for a consumer"""

    def __init__(self, asset_prop: str):
        connectedAssetURL = (
            ac.platform_url
            + "/servers/"
            + ac.server_name
            + "/open-metadata/common-services/"
            + service_url_marker
            + "/connected-asset/users/"
            + ac.user_id
        )
        getAsset = connectedAssetURL + "/assets/" + asset_guid

        response = issue_get(getAsset)
        asset = response.json().get("asset")
        if not asset:
            process_error_response(serverName, "fixme", serverPlatformURL, response)
            return asset

        print(json.dumps(response.json(), indent=4))
        #   elementHeader = asset.get('elementHeader')
        self.elementType = asset.get("type")
        self.assetTypeName = self.elementType.get("typeName")
        self.assetSuperTypes = self.elementType.get("superTypeNames")
        self.guid = asset.get("guid")
        #    self.assetProperties = asset.get('assetProperties')
        self.assetQualifiedName = self.asset.get("qualifiedName")
        self.assetDisplayName = self.asset.get("displayName")
        #    self.assetCatalogBean = self.assetProperties.get('description')
        #    self.assetOwner = self.assetProperties.get('owner')
        self.assetOrigin = self.assetProperties.get("otherOriginValues")
        self.assetOwnerType = self.assetProperties.get("ownerTypeName")
        self.assetZones = self.assetProperties.get("zoneMembership")
        self.assetLatestChange = self.assetProperties.get("latestChange")
        if not self.guid:
            self.guid = "<null>"
        if not self.assetDisplayName:
            self.assetDisplayName = "<none>"
        print(self.assetDisplayName + " [" + self.guid + "]")
        if not self.assetQualifiedName:
            self.assetQualifiedName = "<null>"
        print("  qualifiedName: " + self.assetQualifiedName)
        if self.assetCatalogBean:
            print("  description:   " + self.assetCatalogBean)
        print(
            "  type:          "
            + self.assetTypeName
            + " [%s]" % ", ".join(map(str, assetSuperTypes))
        )
        if self.assetOwner:
            print(
                "  owner:         " + self.assetOwner + " [" + self.assetOwnerType + "]"
            )
        if self.assetOrigin:
            self.contact = self.assetOrigin.get("contact")
            self.dept = self.assetOrigin.get("originatingDept")
            self.org = self.assetOrigin.get("originatingOrganization")
            print(
                "  origin:        contact="
                + self.contact
                + ", dept="
                + self.dept
                + ", org="
                + self.org
            )
        if self.assetZones:
            print("  zones:         " + "%s" % ", ".join(map(str, self.assetZones)))
        if self.assetLatestChange:
            print("  latest change: " + self.assetLatestChange)
