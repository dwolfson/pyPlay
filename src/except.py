import os
import sys
from src.egeria_client.util_exp import (
    issue_data_post,
    process_error_response,
    print_guid_list,
    get_last_guid,
    issue_post,
    issue_get,
    validate_url,
    OMAGCommonErrorCode,
    InvalidParameterException,
)


# raise InvalidParameterException(
#     OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["message_template"],
#     "main",
#     __name__,
#     "foo",
#     "none",
# )


try:
    result = validate_url("http://moo", "junk", None)
    print("success")

except InvalidParameterException as e:
    print(e.error_msg)
    print(e.message_id)
    print(e.message_template)
    print(e.http_error_code)
    print(e.user_action)
    print(e.params)
    sys.exit()
print("squeeky")
