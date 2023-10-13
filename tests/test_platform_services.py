from egeria_client.platform_services import Platform


class TestPlatform:
    def test_activate_server(self):
        p_client = Platform("moo", "https://127.0.0.1:9443", "garygeeke")
        response = p_client.activate_server()
        assert response.status_code == 200

    def test_de_activate_server(self):
        p_client = Platform("moo", "https://127.0.0.1:9443", "garygeeke")
        response = p_client.activate_server()
        assert response.status_code == 200

    def test_list_servers(self):
        p_client = Platform("moo", "https://127.0.0.1:9443", "garygeeke")
        response = p_client.activate_server()
        assert response.status_code == 200
