import os
import sys
from src.egeria_client.utils import (
    issue_data_post,
    process_error_response,
    print_guid_list,
    get_last_guid,
    issue_post,
    issue_get,
    validate_url,
    ExceptionMessageDefinition,
    OMAGCommonErrorCode,
    InvalidParameterException,
)

t = ExceptionMessageDefinition(
    OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["http_error_code"],
    OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["message_id"],
    OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["message_template"],
    OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["system_action"],
    OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["user_action"],
    {"localhost"},
)
# raise InvalidParameterException(
#     t,
#     "main",
#     __name__,
#     "foo",
# )

try:

    url = "http:/1.1.1.1"
    result = validate_url(url, "junk", None)
    print(result)

except InvalidParameterException as e:
    print(f"Exception: {e.message_id} with http code {e.http_error_code}")
    print(f"\t\t   System: {e.system_action}")
    print(f"\t\t   Message: {e.message}")
    print(f"\t\t   User Action: {e.user_action}")

    sys.exit()

print("squeeky")
