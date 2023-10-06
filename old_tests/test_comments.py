#
# This file tests Asset comments
#

import urllib3.exceptions
from requests import ConnectTimeout, ConnectionError

from src.egeria_client.assetLib import print_asset_detail, print_asset_summary, Comment
from src.egeria_client.asset_consumer import AssetConsumer, AssetUniverse, print_comment_list
from src.egeria_client.utils import get_last_guid
from src.egeria_client.util_exp import InvalidParameterException
import time
import sys



my_endpoint = ""
#my_endpoint = "https://localhost:30081"
# my_endpoint = "https://wolfsonnet.me:30081"

try:
# c = AssetConsumer('cocoMDS1', my_endpoint, 'peterprofile')
    c = AssetConsumer('cocoMDS1', my_endpoint, 'peterprofile')

except InvalidParameterException as err:
    print(err.error_msg)
    print(f"Now the message_id only: {err.message_id}")
    print(f"The class name is: {err.class_name}")
    print(f"This occurred in method: {err.action_description}")
    sys.exit()

lg=None
comment_guid_list = []
replies_list = []
comments_list = []
print(c.server_platform_url)


# Find an asset we can play with and set the lg to the last asset GUID we find.
# Print any comments on the asset and then remove them.
try:
    guids = c.find_assets('.*', page_size=20)
    if guids is not None:
        lg = get_last_guid(guids)
        print("Last Guid is " + lg)
        comments_list = c.get_comments(lg)
        if comments_list:
            print(f"There are  {len(comments_list)} comments on this last asset:")
            print_comment_list(comments_list)
            print(f"Now get any direct replies for {len(comments_list)} comments")
            for comment in comments_list:
                print(f"Any replies for {comment}: ")
                if comment.replyCount>0:
                    replies = c.get_comment_replies(lg,comment.comment_guid,debug=True)
                    replies_list.extend(replies)
                    print_comment_list(replies)
            # sys.exit()
            print(f"Now we will remove all the replies we found above")
            for comm_item in replies_list:
                status = c.remove_comment(lg, comm_item.comment_guid)
            # print(f"In removing comment:{comm_item.comment_guid} status was {status}")
            # sys.exit()
            print(f"Now we will remove all the comments we found above")

            for comm_item in comments_list:
                status = c.remove_comment(lg, comm_item.comment_guid)
                # print(f"In removing comment:{comm_item.comment_guid} status was {status}")

            # Now that we have removed the comments lets see if anything is left
            comments_list = c.get_comments(lg)
            if comments_list is None:
                print("All comments successfully removed")
            else:
                print(f"there seem to be {len(comments_list)} comments left?")
                print_comment_list(comments_list)
        else:
            print('No comments to remove')
    else:
        print("There were no matching assets")
except (ConnectionError, ConnectTimeout) as e:
    print(f"A connection error occurred {e}")
except Exception as e:
    print(f"An exception occurred: {e}")

sys.exit()

comment_guid_list.clear()

try:
    # Create three comments and print them
    print('try to add three comments')
    comment_guid_list.append(c.add_comment_to_asset(lg, "First comment",  "QUESTION",True))
    comment_guid_list.append(c.add_comment_to_asset(lg, "Second comment", "QUESTION", False))
    comment_guid_list.append(c.add_comment_to_asset(lg, "Third comment",  "QUESTION", True))

    comments_list = c.get_comments(lg)
    if comments_list:
        print(f"There are now {len(comments_list)} comments on this last asset:")
        print (comment_guid_list)
        # print_comment_list(comments_list)
    # sys.exit()

    print("Now moving on to update the first comment")

    c.update_comment(lg,comment_guid_list[2], "updated Third comment?", "QUESTION",True)
    # sys.exit()
 #  add some replies to the first and second comments
    print("Now adding replies to the first two comments")
    comment_guid_list.append(
        c.add_comment_reply(lg, comment_guid_list[0], "This is an answer to the first question", "ANSWER", True))
    comment_guid_list.append(
        c.add_comment_reply(lg, comment_guid_list[1], "This is an answer to the second question", "ANSWER", True))
    comment_guid_list.append(
        c.add_comment_reply(lg, comment_guid_list[1], "This is another answer to the second question", "ANSWER", True))

    print(f"We now know about these comment: {comment_guid_list}")
    # sys.exit()
    print(f"Now add a comment to the reply {comment_guid_list[-1]}")
    c.add_comment_reply(lg,comment_guid_list[-1], "This is a comment on the reply","ANSWER",True, debug=True)

    comments_list = c.get_comments(lg)
    if comments_list:
        print(f"There are now {len(comments_list)} comments on this last asset:")
        print (comment_guid_list)
        print_comment_list(comments_list)

except Exception as e:
    print(e)



# Add two responses to the first comment

# Delete the second and third comments




# try:
# #    comment_guid = c.add_comment(lg,'This is the first comment', 'OTHER',True)
# #    print('comment guid is: '+ comment_guid)
#     comments_list = c.get_comments(lg)
#     print_comment_list(comments_list)
#     print("updating comments")
# #    comment_guid = c.update_comment(lg, comments_list[1].comment_guid, "Question updated to reflect reality",
# #                                    comments_list[1].comment_type, comments_list[1].is_public)
# #    comments_list2 = c.get_comments(lg)
# #    print_comment_list(comments_list2)
# #    update_comment(lg, comment_guid: str, comment_text: str, comment_type: , True)
# except Exception as e:
#     print(e)