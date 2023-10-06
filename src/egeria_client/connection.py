'''
This is a simple class to create and manage a connection to an Egeria backend

'''

import ...

class Connection():

    def __init__(self, server_name, server_platform_url, user_id):
        self.server_name = server_name
        self.server_platform_url = server_platform_url
        self.user_id = user_id

