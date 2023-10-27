import pytest
from requests import RequestException, ConnectionError, ConnectTimeout

from egeria_client.util_exp import RESTConnectionException

# from egeria_client.client import (
#     Client,
#     InvalidParameterException,
#     PropertyServerException,
# )
from egeria_client.util_exp import (
    OMAGCommonErrorCode,
    EgeriaException,
    InvalidParameterException,
    PropertyServerException,
)

import json
from egeria_client.platform_services import Platform

# import test_client
from contextlib import nullcontext as does_not_raise

import requests

# @pytest.fixture()
# def prepare_platform_test(server_name: str, platform_url: str, user_id: str) -> Client
#     return (Platform(server_name, platform_url, user_id))


class TestPlatform:

    # @pytest.fixture()
    # def prepare_test_client(self, server_name, platform_url, user_id) :

    @pytest.mark.skip(reason="waiting for Egeria bug fix")
    def test_shutdown_platform(self):

        response = None

        with pytest.raises(
            InvalidParameterException, requests.ConnectionError
        ) as excinfo:
            p_client = Platform("moo", "https://127.0.0.1:9443", "garygeeke")
            response = p_client.shutdown_platform()
            if response is not None:
                assert excinfo.value.http_error_code == str(200), "Invalid URL"
                print(excinfo)
            response = p_client.get_platform_origin()

        if excinfo:
            print(
                f"\nException: {excinfo.value.message_id} with http code {excinfo.value.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.value.class_name}")
            print(f"\t\t   Caller: {excinfo.value.action_description}")
            print(f"\t\t   System: {excinfo.value.system_action}")
            print(f"\t\t   Message: {excinfo.value.error_msg}")
            print(f"\t\t   User Action: {excinfo.value.user_action}")

    def test_get_platform_origin(self):
        excinfo = ""
        try:
            p_client = Platform(
                "active-metadata-store", "https://127.0.0.1:9443", "garygeeke"
            )
            response_text = p_client.get_platform_origin()
            print("\n\n" + response_text)
            assert len(response_text) > 0, "Empty response text"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")
            assert False, "Invalid URL?"
        # finally:
        #     if excinfo:
        #         print(f"\n\tException Raised: {excinfo}")
        #         print(
        #             f"\nException: {excinfo.value.message_id} with http code {excinfo.value.http_error_code}"
        #         )
        #         print(f"\t\t   Class: {excinfo.value.class_name}")
        #         print(f"\t\t   Caller: {excinfo.value.action_description}")
        #         print(f"\t\t   System: {excinfo.value.system_action}")
        #         print(f"\t\t   Message: {excinfo.value.error_msg}")
        #         print(f"\t\t   User Action: {excinfo.value.user_action}")

    def test_activate_server_stored_config(self):
        """
        Need to decide if its worth it to broaden out the test cases..for instance
        in this method if there is an exception - such as invalid server name
        then the test case fails because the response is used before set..

        """
        try:
            server = "meow"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.activate_server_stored_config(server)
            print(json.dumps(response, indent=4))
            assert response.get("relatedHTTPCode") == 200

        except (InvalidParameterException, PropertyServerException) as excinfo:
            # assert excinfo.http_error_code == "200"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_shutdown_server(self):
        try:
            server = "meow"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.shutdown_server(server)
            assert response, "Server note available?"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "503"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_list_servers(self):
        try:
            server = "cocoMDS2"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.list_servers()
            print(response)
            assert len(response) > 0, "Empty server list"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "200"
            # assert excinfo.http_error_code == "503"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_shutdown_servers(self):
        p_client = Platform("moo", "https://127.0.0.1:9443", "garygeeke")
        response = p_client.shutdown_servers()
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "server, url, user_id, status_code, expectation",
        [
            (
                "meow",
                "https://google.com",
                "garygeeke",
                404,
                pytest.raises(InvalidParameterException),
            ),
            (
                "cocoMDS2",
                "https://localhost:9443",
                "garygeeke",
                503,
                pytest.raises(InvalidParameterException),
            ),
            (
                "cocoMDS2",
                "https://127.0.0.1:9443",
                "garygeeke",
                200,
                does_not_raise(),
            ),
            (
                "cocoMDS9",
                "https://127.0.0.1:9443",
                "garygeeke",
                404,
                pytest.raises(InvalidParameterException),
            ),
            (
                "cocoMDS2",
                "https://127.0.0.1:9443",
                "",
                404,
                pytest.raises(InvalidParameterException),
            ),
            (
                "cocoMDS2",
                "https://127.0.0.1:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
                "meow",
                404,
                pytest.raises(InvalidParameterException),
            ),
            (
                "cocoMDS2",
                "https://wolfsonnet.me:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
                "woof",
                503,
                pytest.raises(InvalidParameterException),
            ),
            ("", "", "", 400, pytest.raises(InvalidParameterException)),
        ],
    )
    def test_get_active_configuration(
        self, server, url, user_id, status_code, expectation
    ):
        user_pwd = "nonesuch"
        response = requests.Response()

        with expectation as excinfo:
            p_client = Platform(server, url, user_id)
            response = p_client.get_active_configuration()

        if excinfo:
            print(f"\n\tException Raised: {excinfo.typename}")
            print(
                f"\t\t   Egeria Exception: {excinfo.value.message_id} with http code {excinfo.value.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.value.class_name}")
            print(f"\t\t   Caller: {excinfo.value.action_description}")
            print(f"\t\t   System: {excinfo.value.system_action}")
            print(f"\t\t   Message: {excinfo.value.error_msg}")
            print(f"\t\t   User Action: {excinfo.value.user_action}")
            assert excinfo.typename == "InvalidParameterException"
            return

        print(json.dumps(response, indent=4))
        assert response.get("relatedHTTPCode") == status_code, "Invalid URL"

    def test_activate_server_supplied_config(self):
        server = "meow"
        config_body = {
            "class": "OMAGServerConfigResponse",
            "relatedHTTPCode": 200,
            "omagserverConfig": {
                "class": "OMAGServerConfig",
                "versionId": "V2.0",
                "localServerId": "4d310dc6-11ff-4a20-a37c-b21c90c671c2",
                "localServerName": "cocoMDS2",
                "localServerType": "Metadata Access Point",
                "organizationName": "Coco Pharmaceuticals",
                "localServerURL": "https://localhost:9443",
                "localServerUserId": "cocoMDS2npa",
                "localServerPassword": "cocoMDS2passw0rd",
                "maxPageSize": 600,
                "serverSecurityConnection": {
                    "class": "Connection",
                    "headerVersion": 0,
                    "connectorType": {
                        "class": "ConnectorType",
                        "headerVersion": 0,
                        "connectorProviderClassName": "org.odpi.openmetadata.metadatasecurity.samples.CocoPharmaServerSecurityProvider",
                    },
                },
                "eventBusConfig": {
                    "class": "EventBusConfig",
                    "topicURLRoot": "egeria.omag",
                    "configurationProperties": {
                        "producer": {"bootstrap.servers": "localhost:9092"},
                        "consumer": {"bootstrap.servers": "localhost:9092"},
                    },
                    "additionalProperties": {
                        "producer": {"bootstrap.servers": "localhost:9092"},
                        "consumer": {"bootstrap.servers": "localhost:9092"},
                    },
                },
            },
        }

        try:
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.activate_server_supplied_config(config_body, server)
            assert response.get("relatedHTTPCode") == 200

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "503"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_load_archive_files(self):
        pass

    def test_get_active_server_status(self):
        try:
            server = "cocoMDS2"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.get_active_server_status(server)
            print(json.dumps(response, indent=4))
            assert response.get("relatedHTTPCode") == 200, "Invalid URL"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "200"
            # assert excinfo.http_error_code == "503"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_is_server_known(self):
        try:
            server = "meow"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.is_server_known(server)
            print(json.dumps(response, indent=4))
            assert response.get("relatedHTTPCode") == 200, "Invalid URL"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "200"
            # assert excinfo.http_error_code == "503"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_get_active_service_list_for_server(self):
        try:
            server = "cocoMDS2"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.get_active_service_list_for_server(server)
            print(json.dumps(response, indent=4))
            assert response.get("relatedHTTPCode") == 200, "Invalid URL"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "200"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_get_server_status(self):
        try:
            server = "cocoMDS2"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.get_server_status(server)
            print(json.dumps(response, indent=4))
            assert response.get("relatedHTTPCode") == 200, "Invalid URL"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "200"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_get_active_server_list(self):
        try:
            server = "cocoMDS2"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.get_active_server_list()
            print(json.dumps(response, indent=4))
            assert response.get("relatedHTTPCode") == 200, "Invalid URL"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "200"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_shutdown_all_servers(self):
        try:
            server = "cocoMDS2"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.shutdown_all_servers()
            print(json.dumps(response, indent=4))
            assert response.get("relatedHTTPCode") == 200, "Invalid URL"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "503"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")

    def test_check_server_active(self):
        try:
            server = "cocoMDS2"
            p_client = Platform(server, "https://127.0.0.1:9443", "garygeeke")
            response = p_client.check_server_active(server)
            print(f"\n\nserver {server} active state is {str(response)}")
            assert response in (True, False), "Bad Response"

        except (InvalidParameterException, PropertyServerException) as excinfo:
            assert excinfo.http_error_code == "200"
            print(f"\n\tException Raised: {excinfo}")
            print(
                f"\t\t   Exception: {excinfo.message_id} with http code {excinfo.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.class_name}")
            print(f"\t\t   Caller: {excinfo.action_description}")
            print(f"\t\t   System: {excinfo.system_action}")
            print(f"\t\t   Message: {excinfo.error_msg}")
            print(f"\t\t   User Action: {excinfo.user_action}")
